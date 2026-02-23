import logging
from datetime import datetime
import uuid
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.models import Ticket, Message, User
from app.schemas.schemas import MessageCreate
from app.core.config import settings
from app.ai.llm import llm_engine
from app.ai.rag import rag_builder
from app.ai.chroma_client import chroma_client
from app.ai.faiss_index import faiss_manager
from app.core.ws_manager import manager
import asyncio

logger = logging.getLogger(__name__)

async def process_ticket_event_background(ticket_id: UUID, message_id: UUID, user_id: UUID, content: str):
    logger.info(f"AI Processor started for message {message_id} on ticket {ticket_id}")
    
    # We must create our own DB session since this runs in a background thread
    db: Session = SessionLocal()
    try:
        # Retrieve Ticket History
        messages = db.query(Message).filter(Message.ticket_id == ticket_id).order_by(Message.created_at.asc()).all()
        ticket_history = [{"role": "assistant" if m.sender_id != user_id else "user", "content": m.content} for m in messages]
        
        # Chronic Issue Check
        ticket_count = db.query(Ticket).filter(Ticket.user_id == user_id).count()
        is_chronic = ticket_count > 3
        
        # RAG Retrieval
        retrieved_docs = []
        source_ids = []
        try:
            if faiss_manager.index is not None:
                prompt, source_ids = rag_builder.build_prompt(content, ticket_context=ticket_history)
            else:
                prompt, _ = rag_builder.build_prompt(content, ticket_context=ticket_history)
        except Exception as e:
            logger.error(f"RAG Retrieval failed: {e}")
            prompt = f"USER QUERY: {content}\n\nASSISTANT:"

        # LLM Invocation
        schema = {
            "type": "object",
            "properties": {
                "response": {"type": "string"},
                "sentiment": {"type": "string"},
                "summary": {"type": "string"},
                "history_summary": {"type": "string"},
                "draft_response": {"type": "string"},
                "extracted_fields": {"type": "object"},
                "predicted_csat": {"type": "integer"},
                "confidence": {"type": "number"}
            },
            "required": ["response", "sentiment", "summary", "confidence"]
        }
        
        ai_result = llm_engine.generate_response(prompt, schema=schema)
        
        # Find system user
        system_user = db.query(User).filter(User.role == "system").first()
        if not system_user:
            system_user = User(
                id=uuid.uuid4(),
                email="system@antigravity.internal",
                hashed_password="N/A",
                role="system"
            )
            db.add(system_user)
            db.commit()
            db.refresh(system_user)
        
        ai_message = Message(
            ticket_id=ticket_id,
            sender_id=system_user.id,
            content=ai_result.get("response", "Processing failed..."),
            is_internal=True,
            sentiment=ai_result.get("sentiment"),
            summary=ai_result.get("summary"),
            history_summary=ai_result.get("history_summary"),
            draft_response=ai_result.get("draft_response"),
            extracted_fields=ai_result.get("extracted_fields"),
            predicted_csat=ai_result.get("predicted_csat"),
            is_chronic=is_chronic
        )
        db.add(ai_message)
        
        # Updating the ticket status
        db.query(Ticket).filter(Ticket.id == ticket_id).update({
            "status": "in_progress",
            "updated_at": datetime.utcnow()
        })
        
        db.commit()
        db.refresh(ai_message)
        logger.info(f"AI message saved to DB: {ai_message.id}")
        
        # Persistence for RAG
        try:
            chroma_client.add_documents(
                documents=[content, ai_result.get("response")],
                metadatas=[
                    {"ticket_id": str(ticket_id), "message_id": str(message_id), "source": "customer_query"},
                    {"ticket_id": str(ticket_id), "parent_message_id": str(message_id), "source": "ai_response", "sentiment": str(ai_result.get("sentiment")), "is_chronic": str(is_chronic)}
                ],
                ids=[f"user_{message_id}", f"ai_{message_id}"]
            )
            faiss_manager.rebuild()
        except Exception as e:
            logger.error(f"Persistence Failed: {e}")

        # Broadcast via WebSockets
        try:
            if hasattr(ai_message, "id"):
                loop = asyncio.get_event_loop()
                # WebSocket expects dictionary
                msg_data = {
                    "type": "NEW_MESSAGE",
                    "ticket_id": str(ticket_id),
                    "id": str(ai_message.id),
                    "content": ai_message.content,
                    "sender_id": str(system_user.id),
                    "is_internal": True,
                    "sentiment": ai_message.sentiment,
                    "summary": ai_message.summary,
                    "history_summary": ai_message.history_summary,
                    "draft_response": ai_message.draft_response,
                    "extracted_fields": ai_message.extracted_fields,
                    "predicted_csat": ai_message.predicted_csat,
                    "is_chronic": ai_message.is_chronic,
                    "created_at": str(ai_message.created_at)
                }
                
                await manager.broadcast_to_ticket(str(ticket_id), msg_data)
        except Exception as e:
            logger.error(f"WebSocket broadcast failed: {e}")

    except Exception as e:
        logger.error(f"AI Processing fatal error: {e}")
    finally:
        db.close()

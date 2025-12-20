import json
import time
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.llm_engine import llm_engine
from app.services.rag_builder import rag_builder
from app.services.vector_store import vector_service

# DB Setup
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis Setup
redis_client = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    decode_responses=True
)

def process_event(event_data: dict, message_id: str):
    # event_data = {"event_type": "...", "ticket_id": "...", "message_id": "...", "payload": {...}}
    ticket_id = event_data.get("ticket_id")
    event_message_id = event_data.get("message_id") # This is the app-level unique message ID
    
    # 1. Idempotency Check
    dedup_key = f"processed_msg:{event_message_id}"
    if redis_client.get(dedup_key):
        print(f"Skipping duplicate message {event_message_id}")
        return

    print(f"Processing ticket {ticket_id}, message {event_message_id}")
    
    # 2. Build RAG context
    user_query = event_data.get("payload", {}).get("content", "")
    prompt = rag_builder.build_prompt(user_query)
    
    # 3. Generate response with schema
    schema = {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "confidence": {"type": "number"}
        },
        "required": ["response"]
    }
    
    ai_result = llm_engine.generate_response(prompt, schema=schema)
    ai_text = ai_result.get("response", "I'm sorry, I couldn't process that.")

    # 4. Save to Postgres
    db = SessionLocal()
    try:
        from app.models.models import Message, User
        # Find system user or create one
        system_user = db.query(User).filter(User.role == "system").first()
        if not system_user:
            # Create a default system user for the AI
            from uuid import uuid4
            system_user = User(
                id=uuid4(),
                email="system@antigravity.internal",
                hashed_password="N/A",
                role="system"
            )
            db.add(system_user)
            db.commit()
            db.refresh(system_user)

        new_msg = Message(
            ticket_id=ticket_id,
            sender_id=system_user.id,
            content=ai_text,
            is_internal=False
        )
        db.add(new_msg)
        db.commit()
        
        # 5. Notify Frontend via Redis PubSub
        redis_client.publish(f"ticket_updates:{ticket_id}", json.dumps({
            "type": "NEW_MESSAGE",
            "ticket_id": ticket_id,
            "content": ai_text,
            "sender_id": str(system_user.id)
        }))

        # 6. Mark as processed
        redis_client.setex(dedup_key, 86400, "1") # 24h TTL
        
    except Exception as e:
        print(f"Error saving AI response: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    # Ensure consumer group exists
    try:
        redis_client.xgroup_create(settings.TICKET_EVENTS_STREAM, settings.CONSUMER_GROUP, id="0", mkstream=True)
    except Exception:
        pass # Already exists

    print(f"AI Worker started. Listening on {settings.TICKET_EVENTS_STREAM}...")
    
    while True:
        try:
            # Read from stream
            messages = redis_client.xreadgroup(
                groupname=settings.CONSUMER_GROUP,
                consumername="worker_1",
                streams={settings.TICKET_EVENTS_STREAM: ">"},
                count=1,
                block=5000
            )

            if not messages:
                continue

            for stream, msgs in messages:
                for msg_id, data in msgs:
                    event_data = json.loads(data.get("data", "{}"))
                    process_event(event_data, msg_id)
                    # Acknowledge message
                    redis_client.xack(settings.TICKET_EVENTS_STREAM, settings.CONSUMER_GROUP, msg_id)

        except Exception as e:
            print(f"Worker Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

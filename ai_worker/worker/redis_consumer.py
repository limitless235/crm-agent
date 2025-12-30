import json
import redis
import logging
from datetime import datetime
from worker.settings import settings
from worker.llm import llm_engine
from worker.rag import rag_builder
from worker.chroma_client import chroma_client
from worker.faiss_index import faiss_manager
from worker.db import db_manager
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RedisConsumer:
    def __init__(self):
        max_retries = 10
        retry_interval = 2
        self.redis_client = None
        
        for i in range(max_retries):
            try:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST, 
                    port=settings.REDIS_PORT, 
                    decode_responses=True
                )
                self.redis_client.ping()
                break
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                logger.info(f"Redis not ready for AI Worker (attempt {i+1}/{max_retries}). Retrying in {retry_interval}s...")
                time.sleep(retry_interval)

    def setup(self):
        try:
            self.redis_client.xgroup_create(
                settings.TICKET_EVENTS_STREAM, 
                settings.CONSUMER_GROUP, 
                id="0", 
                mkstream=True
            )
        except redis.exceptions.ResponseError:
            pass # Group already exists

    def poll(self):
        logger.info(f"Polling {settings.TICKET_EVENTS_STREAM} (Backpressure: 1 in-flight)...")
        while True:
            try:
                # 1 message at a time = Backpressure protection
                messages = self.redis_client.xreadgroup(
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
                        # Poison Message Protection: Always catch and ACK
                        try:
                            self.process_msg(msg_id, data)
                        except Exception as e:
                            logger.error(f"FAILURE: Poison message detected or fatal error at {msg_id}: {e}")
                        finally:
                            # Always ACK to prevent consumer group stalling
                            self.redis_client.xack(
                                settings.TICKET_EVENTS_STREAM, 
                                settings.CONSUMER_GROUP, 
                                msg_id
                            )
                            logger.info(f"Message {msg_id} processed and ACKed")
            except Exception as e:
                logger.error(f"CRITICAL: Poll loop failure: {e}")

    def process_msg(self, msg_id, data):
        # 1. Parse and Validate Payload (Poison Message Check)
        try:
            raw_data = data.get("data", "{}")
            event_payload = json.loads(raw_data)
        except (json.JSONDecodeError, TypeError):
            logger.error(f"POISON MESSAGE: Invalid JSON format in {msg_id}")
            return

        required_fields = ["ticket_id", "message_id", "content"]
        if not all(field in event_payload for field in required_fields):
            logger.error(f"POISON MESSAGE: Missing core fields in {msg_id}")
            return

        ticket_id = event_payload.get("ticket_id")
        event_message_id = event_payload.get("message_id")
        user_message = event_payload.get("content")
        
        logger.info(f"Processing started: {event_message_id}")

        # 2. Strict Idempotency Check (SETNX + TTL)
        dedup_key = f"processed_msg:{event_message_id}"
        # If SETNX fails, it means it's already being processed or finished
        is_new = self.redis_client.set(dedup_key, "processing", nx=True, ex=settings.IDEMPOTENCY_TTL)
        if not is_new:
            logger.info(f"Skipping: Message {event_message_id} already processed or in-progress")
            return

        # 3. Fetch Ticket History for context
        ticket_history = db_manager.get_ticket_history(ticket_id)
        logger.info(f"Context: Retrieved {len(ticket_history)} historical messages")

        # 3.1 Advanced Productivity: Chronic Issue Detection
        user_id = db_manager.get_user_id_from_ticket(ticket_id)
        is_chronic = False
        if user_id:
            ticket_count = db_manager.get_user_ticket_count(user_id, days=30)
            is_chronic = ticket_count > 3 # Define threshold for "Chronic"
            if is_chronic:
                logger.info(f"PRODUCTIVITY: Chronic issue detected for user {user_id} ({ticket_count} tickets in 30d)")

        # 4. Graceful Degradation: FAISS Availability
        retrieved_docs = []
        source_ids = []
        try:
            if faiss_manager.index is not None:
                prompt, source_ids = rag_builder.build_prompt(user_message, ticket_context=ticket_history)
                logger.info(f"RAG: FAISS retrieval successful ({len(source_ids)} hits)")
            else:
                logger.warning("DEGRADATION: FAISS unavailable. Proceeding without context.")
                prompt, _ = rag_builder.build_prompt(user_message, ticket_context=ticket_history)
        except Exception as e:
            logger.error(f"DEGRADATION: Retrieval failed: {e}")
            prompt, _ = f"USER QUERY: {user_message}\n\nASSISTANT:", []

        # 4. LLM Invocation with Fallback
        logger.info(f"LLM: Invoking for {event_message_id}")
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
        
        fallback_used = "yes" if ai_result.get("fallback") else "no"
        logger.info(f"Processing end: {event_message_id} (Fallback: {fallback_used})")

        # 5. Redis Output Contract (Enhanced for Productivity Agent)
        response_event = {
            "ticket_id": str(ticket_id),
            "message_id": str(event_message_id),
            "response": ai_result.get("response"),
            "sentiment": ai_result.get("sentiment"),
            "summary": ai_result.get("summary"),
            "history_summary": ai_result.get("history_summary"),
            "draft_response": ai_result.get("draft_response"),
            "extracted_fields": ai_result.get("extracted_fields"),
            "predicted_csat": ai_result.get("predicted_csat"),
            "is_chronic": is_chronic,
            "confidence": float(ai_result.get("confidence", 0.0)),
            "sources": source_ids,
            "model": settings.PROJECT_NAME,
            "generated_at": datetime.utcnow().isoformat()
        }

        # 6. Write Output Stream (Reliable)
        try:
            self.redis_client.xadd(settings.AI_RESPONSES_STREAM, {"data": json.dumps(response_event)})
            logger.info(f"Response written: {settings.AI_RESPONSES_STREAM}")
        except Exception as e:
            logger.error(f"CRITICAL: Failed to write to output stream: {e}")
            # Do NOT return; we still want to update state if possible or let the ACK happen

        # 7. Persistence (Graceful Degradation) - Index both User and AI for future RAG
        try:
            chroma_client.add_documents(
                documents=[user_message, ai_result.get("response")],
                metadatas=[
                    {
                        "ticket_id": str(ticket_id), 
                        "message_id": str(event_message_id),
                        "source": "customer_query"
                    },
                    {
                        "ticket_id": str(ticket_id), 
                        "parent_message_id": str(event_message_id),
                        "source": "ai_response",
                        "sentiment": str(ai_result.get("sentiment") or "Unknown"),
                        "summary": str(ai_result.get("summary") or ""),
                        "is_chronic": str(is_chronic)
                    }
                ],
                ids=[f"user_{event_message_id}", f"ai_{event_message_id}"]
            )
            logger.info(f"Persistence: Chroma write successful (Indexed 2 docs)")
        except Exception as e:
            logger.error(f"DEGRADATION: Chroma persistence failed: {e}")

        # 8. Derived Update (Graceful Degradation)
        try:
            faiss_manager.rebuild()
        except Exception as e:
            logger.error(f"DEGRADATION: FAISS rebuild failed: {e}")

        # 9. Mark as complete in Dedup
        self.redis_client.set(dedup_key, "done", ex=settings.IDEMPOTENCY_TTL)

redis_consumer = RedisConsumer()

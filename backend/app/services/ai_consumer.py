import json
import redis
import time
import uuid
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.models import Message, User
from app.core.config import settings
from app.core.ws_manager import manager

def consume_ai_responses():
    max_retries = 10
    retry_interval = 2
    redis_client = None
    
    for i in range(max_retries):
        try:
            redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True
            )
            redis_client.ping()
            break
        except Exception as e:
            if i == max_retries - 1:
                raise e
            print(f"Redis not ready for AI Consumer (attempt {i+1}/{max_retries}). Retrying in {retry_interval}s...")
            time.sleep(retry_interval)

    stream_name = "ai_responses"
    group_name = "backend_response_group"
    
    try:
        redis_client.xgroup_create(stream_name, group_name, id="0", mkstream=True)
    except:
        pass # Already exists

    print(f"Backend AI Consumer started. Listening on {stream_name}...")

    while True:
        try:
            messages = redis_client.xreadgroup(group_name, "backend_1", {stream_name: ">"}, count=1, block=5000)
            if not messages:
                continue

            for _, msgs in messages:
                for msg_id, data in msgs:
                    payload = json.loads(data.get("data", "{}"))
                    
                    ticket_id = payload.get("ticket_id")
                    content = payload.get("response")
                    sentiment = payload.get("sentiment")
                    summary = payload.get("summary")
                    history_summary = payload.get("history_summary")
                    draft_response = payload.get("draft_response")
                    extracted_fields = payload.get("extracted_fields")
                    predicted_csat = payload.get("predicted_csat")
                    is_chronic = payload.get("is_chronic", False)
                    
                    if not ticket_id or not content:
                        redis_client.xack(stream_name, group_name, msg_id)
                        continue

                    db = SessionLocal()
                    try:
                        # Find system user
                        system_user = db.query(User).filter(User.role == "system").first()
                        if not system_user:
                            # Create system user if missing
                            system_user = User(
                                id=uuid.uuid4(),
                                email="system@antigravity.internal",
                                hashed_password="N/A",
                                role="system"
                            )
                            db.add(system_user)
                            db.commit()
                            db.refresh(system_user)

                        # Save message
                        new_msg = Message(
                            id=uuid.uuid4(),
                            ticket_id=ticket_id,
                            sender_id=system_user.id,
                            content=content,
                            is_internal=True,
                            sentiment=sentiment,
                            summary=summary,
                            history_summary=history_summary,
                            draft_response=draft_response,
                            extracted_fields=extracted_fields,
                            predicted_csat=predicted_csat,
                            is_chronic=is_chronic
                        )
                        db.add(new_msg)
                        db.commit()

                        # Notify Frontend via PubSub / WS
                        # In the current simple setup, we broadcast to the WS manager
                        # but in a scaled setup, this would be a separate PubSub listener.
                        # For now, we'll try to broadcast if the manager is in the same process,
                        # but since this runs in a separate worker, we should use REDIS PUB/SUB.
                        
                        notification = json.dumps({
                            "type": "NEW_MESSAGE",
                            "ticket_id": ticket_id,
                            "id": str(new_msg.id),
                            "content": content,
                            "sender_id": str(system_user.id),
                            "is_internal": True,
                            "sentiment": sentiment,
                            "summary": summary,
                            "history_summary": history_summary,
                            "draft_response": draft_response,
                            "extracted_fields": extracted_fields,
                            "predicted_csat": predicted_csat,
                            "is_chronic": is_chronic,
                            "created_at": str(new_msg.created_at)
                        })
                        redis_client.publish(f"ticket_updates:{ticket_id}", notification)

                    except Exception as e:
                        print(f"Error persisting AI response: {e}")
                        db.rollback()
                    finally:
                        db.close()

                    redis_client.xack(stream_name, group_name, msg_id)

        except Exception as e:
            print(f"Consumer error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    consume_ai_responses()

import json
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.models import Ticket, Message
from app.schemas.schemas import TicketCreate, MessageCreate
from app.core.config import settings
import redis

# Initialize Redis
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def create_ticket(db: Session, obj_in: TicketCreate, user_id: UUID):
    db_ticket = Ticket(
        title=obj_in.title,
        priority=obj_in.priority,
        user_id=user_id,
        status="open"
    )
    db.add(db_ticket)
    db.flush() # Get ID

    db_message = Message(
        ticket_id=db_ticket.id,
        sender_id=user_id,
        content=obj_in.initial_message,
        is_internal=False
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_ticket)

    # Push to Redis Stream for AI Worker
    event = {
        "event_type": "TICKET_CREATED",
        "ticket_id": str(db_ticket.id),
        "message_id": str(db_message.id),
        "user_id": str(user_id),
        "content": obj_in.initial_message
    }
    try:
        redis_client.xadd("ticket_events", {"data": json.dumps(event)})
    except Exception as e:
        print(f"Warning: Failed to enqueue ticket to Redis AI worker: {e}")

    return db_ticket

def add_message(db: Session, ticket_id: UUID, obj_in: MessageCreate, sender_id: UUID):
    db_message = Message(
        ticket_id=ticket_id,
        sender_id=sender_id,
        content=obj_in.content,
        is_internal=False
    )
    db.add(db_message)
    
    # Update ticket updated_at
    db.query(Ticket).filter(Ticket.id == ticket_id).update({"updated_at": func.now()})
    
    db.commit()
    db.refresh(db_message)

    # Push to Redis Stream
    event = {
        "event_type": "MESSAGE_RECEIVED",
        "ticket_id": str(ticket_id),
        "message_id": str(db_message.id),
        "user_id": str(sender_id),
        "content": obj_in.content
    }
    try:
        redis_client.xadd("ticket_events", {"data": json.dumps(event)})
    except Exception as e:
        print(f"Warning: Failed to enqueue message to Redis AI worker: {e}")

    return db_message

def get_tickets(db: Session, user_id: UUID, role: str, filter_user_id: UUID = None):
    if role == "admin":
        query = db.query(Ticket)
        if filter_user_id:
            query = query.filter(Ticket.user_id == filter_user_id)
        return query.all()
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def close_ticket(db: Session, ticket_id: UUID):
    db.query(Ticket).filter(Ticket.id == ticket_id).update({"status": "closed", "updated_at": func.now()})
    db.commit()
    # Optional: Broadcast closure via Redis if needed
    return True

def get_ticket_messages(db: Session, ticket_id: UUID):
    return db.query(Message).filter(Message.ticket_id == ticket_id).order_by(Message.created_at.asc()).all()

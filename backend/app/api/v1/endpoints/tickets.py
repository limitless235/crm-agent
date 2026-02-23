from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import schemas
from app.services import ticket_service
from app.models.models import User
from app.core.ws_manager import manager
import bleach
from uuid import UUID

router = APIRouter()

def sanitize_content(content: str) -> str:
    # Basic sanitization: strip HTML tags
    return bleach.clean(content, tags=[], strip=True)

@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_in: schemas.TicketCreate,
    current_user: User = Depends(deps.get_current_user),
    background_tasks: BackgroundTasks,
) -> Any:
    ticket_in.initial_message = sanitize_content(ticket_in.initial_message)
    return ticket_service.create_ticket(db, obj_in=ticket_in, user_id=current_user.id, background_tasks=background_tasks)

@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_id: str = None
) -> Any:
    filter_user_id = None
    if user_id and current_user.role == "admin":
        from uuid import UUID
        filter_user_id = UUID(user_id)
    return ticket_service.get_tickets(db, user_id=current_user.id, role=current_user.role, filter_user_id=filter_user_id)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def read_ticket(
    ticket_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    ticket = db.query(ticket_service.Ticket).filter(ticket_service.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # In production, check if user has access
    return ticket

@router.get("/{ticket_id}/messages", response_model=List[schemas.Message])
def read_messages(
    ticket_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # In production, check if user has access to ticket
    return ticket_service.get_ticket_messages(db, ticket_id=ticket_id)

@router.post("/{ticket_id}/messages", response_model=schemas.Message)
def post_message(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: UUID,
    message_in: schemas.MessageCreate,
    current_user: User = Depends(deps.get_current_user),
    background_tasks: BackgroundTasks,
) -> Any:
    message_in.content = sanitize_content(message_in.content)
    return ticket_service.add_message(db, ticket_id=ticket_id, obj_in=message_in, sender_id=current_user.id, background_tasks=background_tasks)

@router.patch("/{ticket_id}/close", response_model=schemas.Ticket)
def close_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can close tickets")
    ticket_service.close_ticket(db, ticket_id=ticket_id)
    # Return the updated ticket
    return db.query(ticket_service.Ticket).filter(ticket_service.Ticket.id == ticket_id).first()

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from jose import jwt
from app.core.config import settings
# ... existing imports ...

@router.websocket("/ws/{ticket_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    ticket_id: str,
    token: str = None
):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # Optional: check if user has access to ticket_id specifically
    except:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, ticket_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WS messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, ticket_id)

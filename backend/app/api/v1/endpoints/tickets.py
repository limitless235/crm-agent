from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import schemas
from app.services import ticket_service
from app.models.models import User
from app.core.ws_manager import manager
import bleach

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
) -> Any:
    ticket_in.initial_message = sanitize_content(ticket_in.initial_message)
    return ticket_service.create_ticket(db, obj_in=ticket_in, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return ticket_service.get_tickets(db, user_id=current_user.id, role=current_user.role)

@router.get("/{ticket_id}/messages", response_model=List[schemas.Message])
def read_messages(
    ticket_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # In production, check if user has access to ticket
    return ticket_service.get_ticket_messages(db, ticket_id=ticket_id)

@router.post("/{ticket_id}/messages", response_model=schemas.Message)
def post_message(
    *,
    db: Session = Depends(deps.get_db),
    ticket_id: str,
    message_in: schemas.MessageCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    message_in.content = sanitize_content(message_in.content)
    return ticket_service.add_message(db, ticket_id=ticket_id, obj_in=message_in, sender_id=current_user.id)

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

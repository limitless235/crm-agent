from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: str = "user"

class UserCreate(UserBase):
    password: Optional[str] = None

class GoogleAuthRequest(BaseModel):
    credential: str  # The Google ID token

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class User(UserBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Ticket Schemas
class TicketBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    priority: str = "medium"

class TicketCreate(TicketBase):
    initial_message: str = Field(..., min_length=1, max_length=4000)

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class Ticket(TicketBase):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Message Schemas
class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000)

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: UUID
    ticket_id: UUID
    sender_id: UUID
    is_internal: bool
    sentiment: Optional[str] = None
    summary: Optional[str] = None
    history_summary: Optional[str] = None
    draft_response: Optional[str] = None
    extracted_fields: Optional[Dict[str, Any]] = None
    predicted_csat: Optional[int] = None
    is_chronic: bool = False
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None

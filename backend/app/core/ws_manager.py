from typing import List, Dict
from fastapi import WebSocket
import asyncio
import json
from app.core.config import settings
import redis.asyncio as redis

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    async def connect(self, websocket: WebSocket, ticket_id: str):
        await websocket.accept()
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        self.active_connections[ticket_id].append(websocket)
        
        # Start a background task for this ticket if not already listening
        # For simplicity in this phase, we manage connections. 
        # Real-time pubsub will be hooked here by the worker/backend.

    def disconnect(self, websocket: WebSocket, ticket_id: str):
        if ticket_id in self.active_connections:
            self.active_connections[ticket_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_ticket(self, ticket_id: str, message: dict):
        if ticket_id in self.active_connections:
            for connection in self.active_connections[ticket_id]:
                await connection.send_json(message)

manager = ConnectionManager()

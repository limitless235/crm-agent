from typing import List, Dict
from fastapi import WebSocket
import asyncio
import json
from app.core.config import settings
import redis.asyncio as redis

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        self._pubsub_task = None

    async def connect(self, websocket: WebSocket, ticket_id: str):
        await websocket.accept()
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        self.active_connections[ticket_id].append(websocket)
        
        # Start the global PubSub listener if not already running
        if self._pubsub_task is None:
            self._pubsub_task = asyncio.create_task(self._listen_to_redis())

    def disconnect(self, websocket: WebSocket, ticket_id: str):
        if ticket_id in self.active_connections:
            self.active_connections[ticket_id].remove(websocket)
            if not self.active_connections[ticket_id]:
                del self.active_connections[ticket_id]

    async def _listen_to_redis(self):
        pubsub = self.redis_client.pubsub()
        # Listen to all ticket updates
        await pubsub.psubscribe("ticket_updates:*")
        
        async for message in pubsub.listen():
            if message['type'] == 'pmessage':
                channel = message['channel']
                ticket_id = channel.split(':')[-1]
                data = json.loads(message['data'])
                await self.broadcast_to_ticket(ticket_id, data)

    async def broadcast_to_ticket(self, ticket_id: str, message: dict):
        if ticket_id in self.active_connections:
            for connection in self.active_connections[ticket_id]:
                try:
                    await connection.send_json(message)
                except:
                    # Connection might be dead
                    pass

manager = ConnectionManager()

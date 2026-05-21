from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Cliente conectado: {client_id}")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        print(f"Cliente desconectado: {client_id}")

    async def send_chunk(self, client_id: str, text: str):
        ws = self.active_connections.get(client_id)
        if ws:
            await ws.send_json({"type": "chunk", "text": text})

    async def send_done(self, client_id: str):
        ws = self.active_connections.get(client_id)
        if ws:
            await ws.send_json({"type": "done"})

    async def send_error(self, client_id: str, message: str):
        ws = self.active_connections.get(client_id)
        if ws:
            await ws.send_json({"type": "error", "message": message})

manager = ConnectionManager()
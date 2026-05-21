from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_server.manager import manager
from text_pipeline.processor import stream_response

router = APIRouter()

@router.websocket("/ws/chat/{client_id}")
async def chat_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            messages = data.get("messages", [])

            if not messages:
                await manager.send_error(client_id, "No messages here :c")
                continue

            await stream_response(
                messages=messages,
                on_chunk=manager.send_chunk,
                client_id=client_id
            )
            await manager.send_done(client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        await manager.send_error(client_id, str(e))
        manager.disconnect(client_id)
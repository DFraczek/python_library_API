
import asyncio
import datetime

import psutil
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/status")
async def server_status(websocket: WebSocket) -> None:
    """Stream server status and resource usage over a WebSocket connection.

    Sends the server status, current timestamp, CPU usage, and RAM usage
    as JSON every five seconds.

    Args:
        websocket: The WebSocket connection established with the client.
    """
    await websocket.accept()

    try:
        while True:
            data = {
                "status": "online",
                "timestamp": datetime.datetime.now().isoformat(),
                "cpu_usage": f"{psutil.cpu_percent()}%",
                "ram_usage": f"{psutil.virtual_memory().percent}%",
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("WebSocket client disconnected.")

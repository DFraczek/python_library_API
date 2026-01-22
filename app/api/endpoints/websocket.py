import asyncio
import datetime
import psutil
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/status")
async def server_status(websocket: WebSocket) -> None:
    """
    Asynchroniczny WebSocket zwracający aktualne informacje o serwerze w formacie JSON.

    Wysyła dane o statusie, czasie,
    użyciu procesora i pamięci RAM co 5 sekund.

    Args:
        websocket (WebSocket): Obiekt połączenia WebSocket.
    """
    await websocket.accept()
    try:
        while True:
            data = {
                "status": "online",
                "timestamp": datetime.datetime.now().isoformat(),
                "cpu_usage": f"{psutil.cpu_percent()}%",
                "ram_usage": f"{psutil.virtual_memory().percent}%"
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Klient WebSocket rozłączył się.")
    return None
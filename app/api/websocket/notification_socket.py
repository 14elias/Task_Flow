# app/api/websocket/notification_socket.py
import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Security
from typing import Annotated

from app.core.websocket_manager import manager
from app.core.config import settings
from app.api.deps import get_current_active_user
from app.models.user import User # you said you have security; adapt if needed

router = APIRouter()

@router.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket, current_user: Annotated[User, Security(get_current_active_user, scopes=["me"])]):
    """
    Client connects with ws://.../ws/notifications?token=<jwt>.
    get_user_id_from_ws_token should validate the JWT and return the user_id.
    """
    # authenticate and retrieve user_id (adapt this call to your existing auth helper)
    try:
        user_id = current_user.id
    except Exception:
        # security helper should close and raise if invalid
        return

    await websocket.accept()
    await manager.connect(user_id, websocket)

    # send recent history on connect
    try:
        history = await manager.get_history_for_user(user_id)
        for item in history:
            await websocket.send_text(json.dumps(item))
    except Exception:
        pass

    try:
        while True:
            # read to detect disconnects and support pings. We ignore incoming payloads.
            try:
                _ = await websocket.receive_text()
            except WebSocketDisconnect:
                break
            except Exception:
                # no incoming message — just continue. keepalive handled by server/client
                await asyncio.sleep(0.1)
    finally:
        await manager.disconnect(user_id, websocket)

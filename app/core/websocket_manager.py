# app/core/websocket_manager.py
import asyncio
import json
import logging
from typing import Dict, Set
import redis.asyncio as aioredis

from .config import settings

logger = logging.getLogger("websocket.manager")

REDIS_PUB_URL = settings.REDIS_PUB_URL
HISTORY_LEN = settings.NOTIF_HISTORY_LEN

class WebSocketManager:
    def __init__(self):
        # map user_id -> set of WebSocket connections
        self.active_connections: Dict[int, Set] = {}
        self._redis = None
        self._listen_task = None
        self._lock = asyncio.Lock()
        self._started = False

    async def startup(self):
        if self._started:
            return
        self._redis = aioredis.from_url(REDIS_PUB_URL, decode_responses=True)
        self._listen_task = asyncio.create_task(self._redis_listener())
        self._started = True
        logger.info("WebSocketManager started")

    async def shutdown(self):
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass
        if self._redis:
            await self._redis.close()
        self._started = False
        logger.info("WebSocketManager stopped")

    async def connect(self, user_id: int, websocket):
        async with self._lock:
            self.active_connections.setdefault(user_id, set()).add(websocket)
        logger.debug("user %s connected; total %s", user_id, len(self.active_connections[user_id]))

    async def disconnect(self, user_id: int, websocket):
        async with self._lock:
            conns = self.active_connections.get(user_id)
            if not conns:
                return
            conns.discard(websocket)
            if not conns:
                self.active_connections.pop(user_id, None)
        logger.debug("user %s disconnected", user_id)

    async def send_to_user(self, user_id: int, message: dict):
        conns = self.active_connections.get(user_id)
        if not conns:
            return
        text = json.dumps(message)
        to_remove = []
        for ws in list(conns):
            try:
                await ws.send_text(text)
            except Exception as exc:
                logger.warning("send error: %s", exc)
                to_remove.append(ws)
        for ws in to_remove:
            await self.disconnect(user_id, ws)

    async def _redis_listener(self):
        """
        Single background task that PSUBSCRIBEs to notifications:user:* pattern
        and fans out each message to the local in-memory connections.
        """
        pubsub = self._redis.pubsub()
        pattern = "notifications:user:*"
        await pubsub.psubscribe(pattern)
        logger.info("Subscribed to Redis pattern %s", pattern)
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if not message:
                    await asyncio.sleep(0.01)
                    continue
                # message example: {'type':'pmessage', 'pattern':'notifications:user:*', 'channel':'notifications:user:12', 'data':'{"..."}'}
                channel = message.get("channel")
                data = message.get("data")
                if not channel or not data:
                    continue
                try:
                    user_id = int(channel.split(":")[-1])
                except Exception:
                    logger.warning("invalid channel: %s", channel)
                    continue
                try:
                    payload = json.loads(data) if isinstance(data, str) else {"raw": data}
                except Exception:
                    payload = {"raw": data}
                # deliver to user's WS connections in this process
                await self.send_to_user(user_id, payload)
        except asyncio.CancelledError:
            logger.info("Redis listener cancelled")
        finally:
            try:
                await pubsub.punsubscribe(pattern)
            except Exception:
                pass
            await pubsub.close()

    async def get_history_for_user(self, user_id: int):
        """
        Return last N notifications (oldest first) stored in Redis list notifications:user:{id}:history
        """
        r = self._redis
        key = f"notifications:user:{user_id}:history"
        # lrange 0..(HISTORY_LEN-1) returns newest-first (because we'll LPUSH), so reverse it
        raw = await r.lrange(key, 0, HISTORY_LEN - 1)
        results = []
        for item in reversed(raw):
            try:
                results.append(json.loads(item))
            except Exception:
                results.append({"raw": item})
        return results

# single shared manager instance
manager = WebSocketManager()

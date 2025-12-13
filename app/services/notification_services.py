# app/services/notification_service.py
import json
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.celery_app import celery_app
from app.models.notification import Notification  # adjust import if your models structure differs
from app.crud.crud_user import get_by_id

REDIS_PUB_URL = settings.REDIS_PUB_URL
HISTORY_LEN = settings.NOTIF_HISTORY_LEN

# synchronous redis client for publishing (used from request threads). reusing StrictRedis is fine.
r_sync = redis.StrictRedis.from_url(REDIS_PUB_URL, decode_responses=True)

def _user_channel(user_id: int) -> str:
    return f"notifications:user:{user_id}"

def _user_history_key(user_id: int) -> str:
    return f"notifications:user:{user_id}:history"

async def create_and_publish(db: AsyncSession, user_id: int, payload: dict, send_email: bool = True):
    """
    Persist notification, publish to Redis pubsub, push to history list, and enqueue email.
    - db: AsyncSession
    """

    user = await get_by_id(user_id)
    user_email = user.email

    # 1) persist to DB
    notif = Notification(user_id=user_id, message=payload)
    db.add(notif)
    await db.flush()   # ensure ID created
    await db.commit()
    await db.refresh(notif)

    message = {
        "id": notif.id,
        "user_id": user_id,
        "email": user_email,
        "payload": payload,
        "read": notif.is_read,
        "created_at": notif.created_at.isoformat(),
    }

    # 2) publish to Redis
    channel = _user_channel(user_id)
    try:
        r_sync.publish(channel, json.dumps(message))
    except Exception:
        # logging but do not raise; we don't want to break main flow if Redis temporarily fails
        pass

    # 3) push to per-user history (LPUSH newest-first) and trim
    try:
        hist_key = _user_history_key(user_id)
        r_sync.lpush(hist_key, json.dumps(message))
        r_sync.ltrim(hist_key, 0, HISTORY_LEN - 1)
    except Exception:
        pass

    # 4) enqueue email sending via Celery (non-blocking)
    if send_email:
        try:
            # send task by name to avoid circular imports
            celery_app.send_task("app.celery_tasks.send_email.send_email_task", args=(user_id, message))
        except Exception:
            pass

    return message

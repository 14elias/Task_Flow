# app/celery_tasks/send_email.py
from celery import shared_task, Task
from celery.utils.log import get_task_logger
import redis
import json
from email.message import EmailMessage
from smtplib import SMTP
from app.core.config import settings
from app.core.celery_app import celery_app

logger = get_task_logger(__name__)
r = redis.StrictRedis.from_url(settings.REDIS_PUB_URL, decode_responses=True)

class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    retry_kwargs = {"max_retries": 3, "countdown": 5}
    retry_backoff = True
    retry_backoff_max = 600


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True,
    name="app.celery_tasks.send_email.send_email_task",
)
def send_email_task(self, user_id: int, message: dict):
    """
    Send a notification email to user. This task runs in Celery worker.
    message.payload may include 'email' override; otherwise you should look up user email in DB.
    For demonstration we guess an email if none provided — replace this with DB lookup in real code.
    """

    try:
        recipient = message.get("email") or f"user{user_id}@example.com"
        subject = f"[Taskflow] Notification: {message.get('type')}"
        body = json.dumps(message, indent=2)

        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(msg)

        # publish result to user's channel so frontends can see email_sent
        r.publish(f"notifications:user:{user_id}", json.dumps({"type": "email_sent", "notif_id": message.get("id")}))
        return {"status": "sent"}
    except Exception as exc:
        logger.exception("send_email failed: %s", exc)
        try:
            r.publish(f"notifications:user:{user_id}", json.dumps({"type": "email_failed", "notif_id": message.get("id"), "error": str(exc)}))
        except Exception:
            pass
        raise

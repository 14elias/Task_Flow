# app/core/celery_app.py
from celery import Celery
from .config import settings

celery_app = Celery(
    "taskflow",
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    enable_utc=True,
    timezone="UTC",
)

# 🔥 REQUIRED
celery_app.autodiscover_tasks(["app.celery_tasks"])

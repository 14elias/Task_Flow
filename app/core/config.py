from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str

    REDIS_URL: str = "redis://localhost:6379/0"          # default / general
    REDIS_BROKER_URL: str = "redis://localhost:6379/0"   # celery broker
    REDIS_BACKEND_URL: str = "redis://localhost:6379/1"  # celery results
    REDIS_PUB_URL: str = "redis://localhost:6379/4"      # pub/sub + 
    
    CELERY_TASK_QUEUE: str = "default"

    # Notification history length stored in redis list
    NOTIF_HISTORY_LEN: int = 50

    SMTP_HOST: str
    SMTP_PORT: int =587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM: str


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

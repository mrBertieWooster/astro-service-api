from celery import Celery
from app.config import Settings

settings = Settings()

# Настройка Celery
celery_app = Celery(
    "horoscope_worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
)

# Автоматически обнаруживаем задачи в проекте
celery_app.autodiscover_tasks(["app.services"])
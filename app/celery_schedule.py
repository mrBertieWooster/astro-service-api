from celery.schedules import crontab
from app.celery_worker import celery_app

celery_app.conf.beat_schedule = {
    "generate-daily-horoscopes": {
        "task": "app.services.generate_horoscopes.generate_daily_horoscopes",
        "schedule": crontab(hour=0, minute=0),  # Каждый день в 00:00
    },
}
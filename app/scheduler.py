from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone, timedelta
from app.services.horo_generator import generate_horoscopes
import asyncio
import logging

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def run_async_task(task, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Если цикла нет, создаем новый
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(task(*args, **kwargs))
    
    # Если цикл уже запущен, создаем задачу в нем
    return asyncio.create_task(task(*args, **kwargs))

def generate_daily_horoscopes():
    logger.info("Generating daily horoscopes")
    try:
        run_async_task(generate_horoscopes, interval="daily")
        logger.info("Daily horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate daily horoscopes: {str(e)}")

def generate_weekly_horoscopes():
    logger.info("Generating weekly horoscopes")
    try:
        run_async_task(generate_horoscopes, interval="weekly")
        logger.info("Weekly horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate weekly horoscopes: {str(e)}")

def generate_monthly_horoscopes():
    logger.info("Generating monthly horoscopes")
    try:
        run_async_task(generate_horoscopes, interval="monthly")
        logger.info("Monthly horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate monthly horoscopes: {str(e)}")

# Добавляем задачи в планировщик
scheduler.add_job(generate_daily_horoscopes, CronTrigger(hour=0, minute=0, timezone="Europe/Moscow"))
scheduler.add_job(generate_weekly_horoscopes, CronTrigger(day_of_week="mon", hour=0, minute=0, timezone="Europe/Moscow"))
scheduler.add_job(generate_monthly_horoscopes, CronTrigger(day=1, hour=0, minute=0, timezone="Europe/Moscow"))


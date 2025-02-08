from app.config import settings
from app.services.horo_generator import generate_horoscopes
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq_crontab import cron
import logging

logger = logging.getLogger(__name__)

rabbitmq_broker = RabbitmqBroker(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USER,
    password=settings.RABBITMQ_PASSWORD
)

dramatiq.set_broker(rabbitmq_broker)

@cron("0 0 * * *")  # Каждый день в 00:00 UTC
@dramatiq.actor(max_retries=3, time_limit=60000)
async def generate_daily_horoscopes(coords=None):
    logger.info(f'generating daily horoscopes')
    try:
        await generate_horoscopes(interval="daily", coords=coords)
        logger.info("Daily horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate daily horoscopes: {str(e)}")


@cron("0 0 * * 1")  # Каждый понедельник в 00:00 UTC
@dramatiq.actor(max_retries=3, time_limit=60000)
async def generate_weekly_horoscopes(coords=None):
    logger.info(f'generating weekly horoscopes')
    try:
        await generate_horoscopes(interval="weekly", coords=coords)
        logger.info("Weekly horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate weekly horoscopes: {str(e)}")


@cron("0 0 1 * *")  # 1-го числа каждого месяца в 00:00 UTC
@dramatiq.actor(max_retries=3, time_limit=60000)
async def generate_monthly_horoscopes(coords=None):
    logger.info(f'generating monthly horoscopes')
    try:
        await generate_horoscopes(interval="monthly", coords=coords)
        logger.info("Monthly horoscope generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate monthly horoscopes: {str(e)}")
import dramatiq
from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
from app.services.planet_calculation import calculate_planetary_positions, calculate_houses, calculate_aspects
from app.services.ai_clients.openai_client.apenai_horo_generation import generate_horoscope_text
from app.config import settings
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

utc_plus_3 = timezone(timedelta(hours=3))
intervals_mapping = {'daily': 'день', 'weekly': 'неделя', 'monthly': 'месяц'}
signs = list['aries': str, 'taurus': str, 'gemini': str, 'cancer': str, 'leo': str, 'virgo': str, 
             'libra': str, 'scorpio': str, 'sagittarius': str, 'capricorn': str, 'aquarius': str, 'pisces': str]

@dramatiq.actor
def generate_daily_horoscopes(coords=None):
    logger.info(f'generating daily horoscopes')
    generate_horoscopes(coords, 'daily')

@dramatiq.actor
def generate_weekly_horoscopes(coords=None):
    logger.info(f'generating weekly horoscopes')
    generate_horoscopes(coords, 'weekly')

@dramatiq.actor
def generate_monthly_horoscopes(coords=None):
    logger.info(f'generating monthly horoscopes')
    generate_horoscopes(coords, 'monthly')


def generate_horoscopes(interval='daily', coords=None):
    """
    Генерирует ежедневные гороскопы для всех знаков зодиака и сохраняет их в базу данных.
    """
    db = SessionLocal()

    
    date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата по МСК

    if not coords:
        coords = settings.DEFAULT_COORDS

    planetary_positions = calculate_planetary_positions(datetime.now(utc_plus_3))
    aspects = calculate_aspects(planetary_positions)
    houses = calculate_houses(datetime.now(utc_plus_3), lat=coords[0], lon=coords[1])

    for sign in signs:
        
        prediction = generate_daily_horoscope(sign, planetary_positions, aspects, houses, intervals_mapping[interval])
        logging.info(f'Horoscope for {sign}: {prediction}')
        
        horoscope = Horoscope(
            sign=sign,
            prediction=prediction,
            date=date,
            type=interval,
            language="ru",
            source="swisseph",
            is_active=True
        )
        db.add(horoscope)
    
    db.commit()
    db.close()


def generate_daily_horoscope(sign, planetary_positions, aspects, houses, interval):
    return generate_horoscope_text(sign, planetary_positions, aspects, houses, interval)
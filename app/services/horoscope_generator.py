from app.celery_worker import celery_app
from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
from app.services.planet_calculation import calculate_planetary_positions, calculate_houses, calculate_aspects
from app.services.ai_clients.openai_client.apenai_horo_generation import generate_horoscope_text
from app.config import settings
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

utc_plus_3 = timezone(timedelta(hours=3))

@celery_app.task
def generate_daily_horoscopes(coords=None):
    """
    Генерирует ежедневные гороскопы для всех знаков зодиака и сохраняет их в базу данных.
    """
    db = SessionLocal()

    signs = list['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    
    date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата по МСК

    if not coords:
        coords = settings.DEFAULT_COORDS

    planetary_positions = calculate_planetary_positions(datetime.now(utc_plus_3))
    aspects = calculate_aspects(planetary_positions)
    houses = calculate_houses(datetime.now(utc_plus_3), lat=coords[0], lon=coords[1])

    for sign in signs:
        
        prediction = generate_daily_horoscope(sign, planetary_positions, aspects, houses)
        logging.info(f'Horoscope for {sign}: {prediction}')
        
        horoscope = Horoscope(
            sign=sign,
            prediction=prediction,
            date=date,
            type="daily",
            language="ru",
            source="swisseph",
            is_active=True
        )
        db.add(horoscope)
    
    db.commit()
    db.close()


def generate_daily_horoscope(sign, planetary_positions, aspects, houses):
    return generate_horoscope_text(sign, planetary_positions, aspects, houses)
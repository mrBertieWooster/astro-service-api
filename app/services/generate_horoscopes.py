from datetime import datetime, timedelta, timezone
from app.celery_worker import celery_app
from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
from app.services.ephemeris import calculate_planetary_positions, generate_horoscope_text

utc_plus_3 = timezone(timedelta(hours=3))

@celery_app.task
def generate_daily_horoscopes():
    """
    Генерирует ежедневные гороскопы для всех знаков зодиака и сохраняет их в базу данных.
    """
    db = SessionLocal()
    signs = set("aries", "taurus", "gemini", "cancer", "leo", "virgo", 
             "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces")
    date = utc_plus_3.date()  # Сегодняшняя дата

    for sign in signs:
        # Рассчитываем положения планет
        planetary_positions = calculate_planetary_positions(utc_plus_3)
        
        # Генерируем текст гороскопа
        prediction = generate_horoscope_text(sign, planetary_positions)
        
        # Создаем запись в базе данных
        horoscope = Horoscope(
            sign=sign,
            prediction=prediction,
            date=date,
            type="daily",
            language="ru",
            source="swisseph",
            is_active=True
        )
        #db.add(horoscope)
    
    #db.commit()
    #db.close()
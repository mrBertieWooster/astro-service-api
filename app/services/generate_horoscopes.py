from datetime import datetime, timedelta, timezone
from app.celery_worker import celery_app
from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
from app.services.ephemeris import calculate_planetary_positions, calculate_houses, calculate_aspects
from app.services.horoscope_generation import generate_horoscope_text

utc_plus_3 = timezone(timedelta(hours=3))

#@celery_app.task
def generate_daily_horoscopes():
    """
    Генерирует ежедневные гороскопы для всех знаков зодиака и сохраняет их в базу данных.
    """
    db = SessionLocal()
    #signs = list['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
    #         'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    signs = ['cancer']
    date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата

    planetary_positions = calculate_planetary_positions(datetime.now(utc_plus_3))
    aspects = calculate_aspects(planetary_positions)
    houses = calculate_houses(datetime.now(utc_plus_3), lat=55.7558, lon=37.6176)  # Пример: ко

    for sign in signs:
        
        # Генерируем текст гороскопа
        prediction = generate_horoscope_text(sign, planetary_positions, aspects, houses)
        print(prediction)
        
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
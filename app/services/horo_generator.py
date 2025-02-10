from app.api.v1.models.horoscope import Horoscope
from app.db.database import async_session
from app.services.planet_calculation import calculate_planetary_positions, calculate_houses, calculate_aspects
from app.services.ai_clients.openai_client.apenai_horo_generation import generate_horoscope_text
from app.config import settings
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import asyncio
import logging

logger = logging.getLogger(__name__)

intervals_mapping = {'daily': 'день', 'weekly': 'неделя', 'monthly': 'месяц'}
signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']


async def generate_horoscopes(interval='daily', coords=None, date=None):
    """
    Асинхронная генерация гороскопов для всех знаков зодиака и сохранение их в базу данных.

    :param interval: Тип интервала (например, 'daily', 'weekly').
    :param coords: Координаты для вычисления домов.
    """
    try:
        async with async_session() as db:
            async with db.begin():  # Начало транзакции
                tasks = [
                    asyncio.create_task(generate_single_horoscope(db, sign, interval, coords))
                    for sign in signs
                ]

                results = await asyncio.gather(*tasks, return_exceptions=True)  # Собираем результаты

                for result in results:
                    if isinstance(result, Exception):  # Проверяем, была ли ошибка
                        logger.error(f"Error while generating horoscope: {str(result)}")
                await db.commit()

    except ValueError as ve:
        logger.error(f"Error in astrological calculations: {str(ve)}")
    except ConnectionError as ce:
        logger.error(f"Failed to connect to external service: {str(ce)}")
    except SQLAlchemyError as se:
        logger.error(f"Database error while saving horoscopes: {str(se)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


async def generate_single_horoscope(db: Session, zodiac_sign: str, interval: str, coords=None):
    """
    Генерирует гороскоп для одного знака зодиака.
    """
    if not isinstance(zodiac_sign, str):  # Добавьте проверку
        raise ValueError(f"Invalid zodiac_sign type: {type(zodiac_sign)}. Expected str.")
    if not coords:
        coords = settings.DEFAULT_COORDS
    
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата по МСК
    coords = settings.DEFAULT_COORDS
    
    try:
        planetary_positions = calculate_planetary_positions(datetime.now(utc_plus_3))
        aspects = calculate_aspects(planetary_positions)
        houses = calculate_houses(datetime.now(utc_plus_3), lat=coords[0], lon=coords[1])
        
        logger.info(f'generating prediction fo sign: {zodiac_sign}')
        
        prediction = await generate_horoscope_text(zodiac_sign, planetary_positions, aspects, houses, intervals_mapping[interval])
        
        horoscope = Horoscope(
            sign=zodiac_sign,
            prediction=prediction,
            date=current_date,
            type=interval,
            language="ru",
            source="swisseph",
            is_active=True,
            created_at=datetime.now().replace(tzinfo=None),
            updated_at=datetime.now().replace(tzinfo=None)
        )
        db.add(horoscope)
        await db.commit()
        await db.refresh(horoscope)
        
        return horoscope
    
    except SQLAlchemyError as se:
        await db.rollback()
        raise
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
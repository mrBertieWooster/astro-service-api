from app.api.v1.models.horoscope import Horoscope
from app.db.database import async_session
from app.services.planet_calculation import calculate_planetary_positions_and_houses, calculate_aspects
from app.services.ai_clients.openai_client.openai_horo_generation import generate_horoscope_text
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import asyncio
import logging

logger = logging.getLogger(__name__)

intervals_mapping = {'daily': 'день', 'weekly': 'неделя', 'monthly': 'месяц'}
signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
             'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']


async def generate_horoscopes(interval='daily'):
    """
    Асинхронная генерация гороскопов для всех знаков зодиака и сохранение их в базу данных.

    :param interval: Тип интервала (например, 'daily', 'weekly').
    :param coords: Координаты для вычисления домов.
    """
    
    loop = asyncio.get_running_loop()
    try:
        tasks = [
            loop.create_task(generate_single_horoscope_task(sign, interval))
            for sign in signs
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)  # Собираем результаты

        for result in results:
            if isinstance(result, Exception):  # Проверяем, была ли ошибка
                logger.error(f"Error while generating horoscope: {str(result)}")

    except ValueError as ve:
        logger.error(f"Error in astrological calculations: {str(ve)}")
        raise
    except ConnectionError as ce:
        logger.error(f"Failed to connect to external service: {str(ce)}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise


async def generate_single_horoscope_task(sign: str, interval: str):
    # Открываем новую сессию для каждой задачи
    async with async_session() as db:
        try:
            await generate_single_horoscope(db, sign, interval)
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to generate or save horoscope for {sign}: {str(e)}")
            raise
            

async def generate_single_horoscope(db: Session, zodiac_sign: str, interval: str, lat: float = None, lon: float = None):
    """
    Генерирует гороскоп для одного знака зодиака.
    """
    if not isinstance(zodiac_sign, str):
        raise ValueError(f"Invalid zodiac_sign type: {type(zodiac_sign)}. Expected str.")
    
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата по МСК
    
    try:
        existing_horoscope = (await db.execute(
            select(Horoscope).filter(
                Horoscope.sign == zodiac_sign,
                Horoscope.date == datetime.now(timezone(timedelta(hours=3))).date(),
                Horoscope.type == interval
            )
        )).scalar_one_or_none()
        if existing_horoscope:
            logger.info(f"Horoscope for {zodiac_sign} already exists for {interval}. Skipping generation.")
            return existing_horoscope
        
        
        planetary_positions = calculate_planetary_positions_and_houses(date=datetime.now(utc_plus_3), latitude=lat, longitude=lon)
        aspects = calculate_aspects(planetary_positions)
        
        logger.info(f'generating prediction fo sign: {zodiac_sign}')
        
        prediction = await generate_horoscope_text(zodiac_sign, planetary_positions, aspects, intervals_mapping[interval])
            
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
        await db.flush()
        await db.refresh(horoscope)
        
        return horoscope
    
    except SQLAlchemyError as se:
        logger.error(f'Error cannot generate single horoscope: {str(se)}')
        await db.rollback()
        raise
    except Exception as e:
        logger.error(f'Error cannot generate single horoscope: {str(e)}')
        raise
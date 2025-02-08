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
signs = list['aries': str, 'taurus': str, 'gemini': str, 'cancer': str, 'leo': str, 'virgo': str, 
             'libra': str, 'scorpio': str, 'sagittarius': str, 'capricorn': str, 'aquarius': str, 'pisces': str]


async def generate_horoscopes(interval='daily', coords=None):
    """
    Асинхронная генерация гороскопов для всех знаков зодиака и сохранение их в базу данных.

    :param interval: Тип интервала (например, 'daily', 'weekly').
    :param coords: Координаты для вычисления домов.
    """

    if not coords:
        coords = settings.DEFAULT_COORDS

    try:
        async with async_session() as db:
            async with db.begin():  # Начало транзакции
                tasks = []
                for sign in signs:
                    task = asyncio.create_task(
                        generate_single_horoscope(
                            db=db,
                            sign=sign,
                            interval=interval,
                            coords=coords
                        )
                    )
                    tasks.append(task)

                # Параллельное выполнение задач
                await asyncio.gather(*tasks)
                await db.commit()

    except ValueError as ve:
        logger.error(f"Error in astrological calculations: {str(ve)}")
    except ConnectionError as ce:
        logger.error(f"Failed to connect to external service: {str(ce)}")
    except SQLAlchemyError as se:
        logger.error(f"Database error while saving horoscopes: {str(se)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")


async def generate_single_horoscope(db: Session, zodiac_sign: str, interval: str):
    """
    Генерирует гороскоп для одного знака зодиака.
    """
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()  # Сегодняшняя дата по МСК
    coords = settings.DEFAULT_COORDS
    
    try:
        planetary_positions = calculate_planetary_positions(datetime.now(utc_plus_3))
        aspects = calculate_aspects(planetary_positions)
        houses = calculate_houses(datetime.now(utc_plus_3), lat=coords[0], lon=coords[1])
        
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
    
    except ValueError as ve:
        raise ValueError(f"Error in astrological calculations: {str(ve)}")
    except ConnectionError as ce:
        raise ConnectionError(f"Failed to connect to external service: {str(ce)}")
    except SQLAlchemyError as se:
        db.rollback()
        raise RuntimeError(f"Database error while saving horoscope: {str(se)}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")
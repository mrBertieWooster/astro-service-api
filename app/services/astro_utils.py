from datetime import datetime
from app.api.v1.models.zodiac import Zodiac
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

logger = logging.getLogger(__name__)

ZODIAC_DATES = {
    "aries": ("03-21", "04-19"),
    "taurus": ("04-20", "05-20"),
    "gemini": ("05-21", "06-20"),
    "cancer": ("06-21", "07-22"),
    "leo": ("07-23", "08-22"),
    "virgo": ("08-23", "09-22"),
    "libra": ("09-23", "10-22"),
    "scorpio": ("10-23", "11-21"),
    "sagittarius": ("11-22", "12-21"),
    "capricorn": ("12-22", "01-19"),
    "aquarius": ("01-20", "02-18"),
    "pisces": ("02-19", "03-20")
}

async def get_zodiac_sign(db: AsyncSession, birth_date: str):
    """
    Определяет знак зодиака по дате рождения и возвращает ID знака из базы.
    """
    month_day = birth_date[5:]  # "MM-DD"
    logger.debug(f'День месяца {month_day}')

    for sign, (start, end) in ZODIAC_DATES.items():
        logger.debug(f'Проверяем: {sign}, старт: {start}, месяц-день: {month_day}, конец: {end}')

        # Обрабатываем знаки, которые охватывают Новый год (например, Козерог: 12-22 — 01-19)
        if start > end:  
            if month_day >= start or month_day <= end:
                logger.debug(f'Определили знак: {sign}')
                result = await db.execute(select(Zodiac).filter(Zodiac.name == sign))
                zodiac = result.scalar_one_or_none()
                return zodiac.id if zodiac else None
        
        # Обычный случай (в пределах одного года)
        elif start <= month_day <= end:
            logger.debug(f'Определили знак: {sign}')
            result = await db.execute(select(Zodiac).filter(Zodiac.name == sign))
            zodiac = result.scalar_one_or_none()
            return zodiac.id if zodiac else None

    return None 


from app.api.v1.models.horoscope import Horoscope, HoroscopeRequest
from app.enums.zodiac import ZodiacSign
from app.db.database import get_db
from app.services.horo_generator import generate_single_horoscope
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from enum import Enum
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class IntervalType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@router.get("/{zodiac_sign}", summary="Получить гороскоп", description="Возвращает гороскоп для указанного знака зодиака.")
async def get_horoscope(
    zodiac_sign: ZodiacSign,
    interval: IntervalType = IntervalType.DAILY,  # По умолчанию на день
    db: AsyncSession = Depends(get_db)):
    
    """
    Получить гороскоп для знака зодиака.
    - **zodiac_sign**: Знак зодиака (например, aries, taurus).
    """
    
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()
    
    if interval == IntervalType.MONTHLY:
        first_day_of_month = current_date.replace(day=1)
        date = first_day_of_month
    else:
        date = current_date
    
    logger.info(f'Request for {interval.value} horoscope for sign {zodiac_sign}')
    
    try:
        horoscope = (
            (await db.execute(
                select(Horoscope).filter(
                    Horoscope.sign == zodiac_sign.value,
                    Horoscope.type == interval.value,
                    Horoscope.date == date
                )
            )).scalar_one_or_none()
        )
        
        if not horoscope: # в базе еще нет, генерируем для конкретного знака
            logger.warning(f'Cannot find horoscope for sign {zodiac_sign} in db for interval {interval.value}')
            try:
                logger.info(f'Try to generate horoscope for sign {zodiac_sign} in-place')
                horoscope = await generate_single_horoscope(db, zodiac_sign.value, interval.value)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate horoscope: {str(e)}")
            
        request_record = HoroscopeRequest(
            sign=zodiac_sign.value,
            type=interval.value,
            horoscope_id=horoscope.id
        )
        db.add(request_record)
        await db.commit()
        
        return {"sign": horoscope.sign, "prediction": horoscope.prediction}

    except SQLAlchemyError as e:
        db.rollback()  # Откатываем транзакцию при ошибке базы данных
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации гороскопа: {str(e)}")
    


@router.post("/", summary="Создать гороскоп", description="Добавляет новый гороскоп в базу данных.")
async def create_horoscope(
    zodiac_sign: str,
    prediction: str,
    db: AsyncSession = Depends(get_db) 
):
    db_horoscope = Horoscope(
        sign=zodiac_sign,
        prediction=prediction,
        date=datetime.now(timezone(timedelta(hours=3))).date(),
        type="manual",  # Тип можно указать явно
        language="ru",
        source="manual",
        is_active=True,
        created_at=datetime.now().replace(tzinfo=None),
        updated_at=datetime.now().replace(tzinfo=None)
    )
    db.add(db_horoscope)
    await db.commit()  # Асинхронный commit
    await db.refresh(db_horoscope)  # Асинхронное обновление объекта

    return db_horoscope

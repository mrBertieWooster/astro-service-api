from app.api.v1.models.horoscope import Horoscope, HoroscopeRequest
from app.db.database import get_db
from app.services.horo_generator import generate_single_horoscope
from app.schemas.horoscope import HoroscopeResponse, HoroscopeRequestSchema
from app.enums.zodiac import IntervalType, ZodiacSign
from app.config import settings
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{zodiac_sign}", summary="Получить гороскоп", description="Возвращает гороскоп для указанного знака зодиака.", response_model=HoroscopeResponse)
async def get_horoscope(zodiac_sign: ZodiacSign, request: HoroscopeRequestSchema, db: AsyncSession = Depends(get_db)):

    """
    Получить гороскоп для знака зодиака.
    - **zodiac_sign**: Знак зодиака (например, aries, taurus).
    """
    
    latitude = request.latitude or settings.DEFAULT_COORDS[0]
    longitude = request.longitude or settings.DEFAULT_COORDS[1]
    sign = zodiac_sign
    
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()
    
    if request.interval == IntervalType.MONTHLY:
        first_day_of_month = current_date.replace(day=1)
        date = first_day_of_month
    else:
        date = current_date
    
    logger.info(f'Request for {request.interval} horoscope for sign {sign}')
    
    try:
        horoscope = (
            (await db.execute(
                select(Horoscope).filter(
                    Horoscope.sign == sign,
                    Horoscope.type == request.interval,
                    Horoscope.date == date
                )
            )).scalar_one_or_none()
        )
        
        if not horoscope: # в базе еще нет, генерируем для конкретного знака
            logger.warning(f'Cannot find horoscope for sign {sign} in db for interval {request.interval}')
            try:
                logger.info(f'Try to generate horoscope for sign {sign} in-place')
                horoscope = await generate_single_horoscope(db, sign, request.interval, latitude, longitude)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate horoscope: {str(e)}")
            
        request_record = HoroscopeRequest(
            sign=sign,
            type=request.interval,
            horoscope_id=horoscope.id
        )
        db.add(request_record)
        await db.commit()
        
        return HoroscopeResponse(sign=horoscope.sign, prediction=horoscope.prediction)

    except SQLAlchemyError as e:
        await db.rollback()  # Откатываем транзакцию при ошибке базы данных
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации гороскопа: {str(e)}")


from app.api.v1.models.horoscope import Horoscope, HoroscopeRequest
from app.db.database import SessionLocal
from app.services.horo_generator import generate_single_horoscope
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta, timezone
from enum import Enum
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ZodiacSign(str, Enum):
    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"

class IntervalType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@router.get("/{zodiac_sign}", summary="Получить гороскоп", description="Возвращает гороскоп для указанного знака зодиака.")
async def get_horoscope(
    zodiac_sign: ZodiacSign,
    interval: IntervalType = IntervalType.DAILY,  # По умолчанию на день
    db: Session = Depends(get_db)):
    
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
        horoscope = db.query(Horoscope).filter(Horoscope.sign == zodiac_sign, Horoscope.type == interval.value, Horoscope.date == date).first()
        if not horoscope: # в базе еще нет, генерируем для конкретного знака
            logger.warning(f'Cannot find horoscope for sign {zodiac_sign} in db for interval {interval.value}')
            try:
                logger.info(f'Try to generate horoscope for sign {zodiac_sign} in-place')
                horoscope = generate_single_horoscope(db, zodiac_sign.value, interval.value)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate horoscope: {str(e)}")
            
        request_record = HoroscopeRequest(
            sign=zodiac_sign.value,
            type=interval.value,
            horoscope_id=horoscope.id
        )
        db.add(request_record)
        db.commit()
        
        return {"sign": horoscope.sign, "prediction": horoscope.prediction}
    
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid sign: {str(ve)}")
    except SQLAlchemyError as e:
        db.rollback()  # Откатываем транзакцию при ошибке базы данных
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        db.close()   
    


@router.post("/")
async def create_horoscope(zodiac_sign: str, prediction: str, db: Session = Depends(get_db)):
    db_horoscope = Horoscope(zodiac_sign=zodiac_sign, prediction=prediction)
    db.add(db_horoscope)
    db.commit()
    db.refresh(db_horoscope)
    return db_horoscope
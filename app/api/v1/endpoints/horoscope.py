from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
from app.services.horo_generator import generate_single_horoscope
from fastapi import APIRouter, Depends, HTTPException
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
    date = datetime.now(utc_plus_3).date()
    
    logger.info(f'Request for {interval.value} horoscope for sign {zodiac_sign}')
    
    try:
        horoscope = db.query(Horoscope).filter(Horoscope.sign == zodiac_sign, Horoscope.type == interval.value, Horoscope.date == date).first()
        if not horoscope: # в базе еще нет, генерируем для конкретного знака
            try:
                horoscope = generate_single_horoscope(db, zodiac_sign.value, interval.value)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to generate horoscope: {str(e)}")
        return {"sign": horoscope.sign, "prediction": horoscope.prediction}
    
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
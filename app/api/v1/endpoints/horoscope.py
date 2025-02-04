from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.models.horoscope import Horoscope
from app.db.database import SessionLocal
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

@router.get("/{zodiac_sign}", summary="Получить гороскоп", description="Возвращает гороскоп для указанного знака зодиака.")
async def get_horoscope(zodiac_sign: ZodiacSign, db: Session = Depends(get_db)):
    """
    Получить гороскоп для знака зодиака.
    - **zodiac_sign**: Знак зодиака (например, aries, taurus).
    """
    logger.info(f'request for horoscope for sign {zodiac_sign}')
    horoscope = db.query(Horoscope).filter(Horoscope.sign == zodiac_sign).first()
    if not horoscope:
        raise HTTPException(status_code=404, detail="Horoscope not found")
    return horoscope

@router.post("/")
async def create_horoscope(zodiac_sign: str, prediction: str, db: Session = Depends(get_db)):
    db_horoscope = Horoscope(zodiac_sign=zodiac_sign, prediction=prediction)
    db.add(db_horoscope)
    db.commit()
    db.refresh(db_horoscope)
    return db_horoscope
from fastapi import APIRouter, Depends
from app.dramatiq_worker import generate_daily_horoscopes, generate_weekly_horoscopes, generate_monthly_horoscopes

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/trigger-daily-horoscopes")
async def trigger_daily_horoscopes():
    """
    Ручной триггер для генерации ежедневных гороскопов.
    """
    generate_daily_horoscopes.send()
    return {"message": "Daily horoscopes generation triggered."}

@router.post("/trigger-weekly-horoscopes")
async def trigger_weekly_horoscopes():
    """
    Ручной триггер для генерации еженедельных гороскопов.
    """
    generate_weekly_horoscopes.send()
    return {"message": "Weekly horoscopes generation triggered."}
from fastapi import APIRouter
from app.scheduler import generate_daily_horoscopes, generate_weekly_horoscopes, generate_monthly_horoscopes


router = APIRouter()

@router.post("/generate/daily")
async def trigger_daily_horoscopes():
    generate_daily_horoscopes()
    return {"message": "Daily horoscope generation started"}

@router.post("/generate/weekly")
async def trigger_weekly_horoscopes():
    generate_weekly_horoscopes()
    return {"message": "Weekly horoscope generation started"}

@router.post("/generate/monthly")
async def trigger_monthly_horoscopes():
    generate_monthly_horoscopes()
    return {"message": "Monthly horoscope generation started"}
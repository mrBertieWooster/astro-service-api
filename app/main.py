from fastapi import FastAPI
from fastapi import HTTPException
from app.api.v1.endpoints.horoscope import router as horoscope_router
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

from fastapi import FastAPI


app = FastAPI()

app.include_router(horoscope_router, prefix="/api/v1/horoscope", tags=["horoscope"])

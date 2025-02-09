from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1.endpoints.horoscope import router as horoscope_router
from app.api.v1.endpoints.compatibility import router as compatibility_router
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(horoscope_router, prefix="/api/v1/horoscope", tags=["horoscope"])
app.include_router(compatibility_router, prefix="/api/v1/compatibility", tags=["compatibility"])

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик всех исключений.
    """
    logging.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please check the server logs."}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Обработчик исключений SQLAlchemy.
    """
    logging.error(f"Database error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error. Please check the server logs."}
    )

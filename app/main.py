from app.api.v1.endpoints.horoscope import router as horoscope_router
from app.api.v1.endpoints.compatibility import router as compatibility_router
from app.api.v1.endpoints.admin_endpoints import router as admin_router
from app.api.v1.endpoints.natal_chart import router as natal_chart_router
from app.scheduler import scheduler
from app.logging_config import LOGGING_CONFIG
from app.exceptions import HoroscopeGenerationError, OpenAIAPIError, DatabaseError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
import logging
import traceback


logging.config.dictConfig(LOGGING_CONFIG)


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting APScheduler...")
    scheduler.start()
    yield
    logger.info("Shutting down APScheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


app.include_router(horoscope_router, prefix="/api/v1/horoscope", tags=["horoscope"])
app.include_router(compatibility_router, prefix="/api/v1/compatibility", tags=["compatibility"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(natal_chart_router, prefix="/api/v1/natal_chart", tags=["natal_chart"])


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Глобальный обработчик исключений, логирующий полный стектрейс.
    """
    if isinstance(exc, RequestValidationError):
        status_code = 422
        error_message = "Ошибка валидации запроса"
    elif isinstance(exc, SQLAlchemyError):
        status_code = 500
        error_message = "Ошибка базы данных"
    else:
        status_code = 500
        error_message = "Неизвестная ошибка"

    logger.error(f"{error_message}: {str(exc)}")
    logger.error(traceback.format_exc())  # Полный стек ошибки

    return JSONResponse(status_code=status_code, content={"error": error_message})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Обработчик исключений SQLAlchemy.
    """
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error. Please check the server logs."}
    )

@app.exception_handler(HoroscopeGenerationError)
async def horoscope_exception_handler(request, exc: HoroscopeGenerationError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Ошибка генерации гороскопа. Попробуйте позже."},
    )

@app.exception_handler(OpenAIAPIError)
async def openai_exception_handler(request, exc: OpenAIAPIError):
    return JSONResponse(
        status_code=502,
        content={"error": "Ошибка запроса к OpenAI", "detail": exc.message},
    )

@app.exception_handler(DatabaseError)
async def database_exception_handler(request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"error": "Ошибка базы данных", "detail": exc.message},
    )
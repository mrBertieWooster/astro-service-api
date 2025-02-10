from app.api.v1.endpoints.horoscope import router as horoscope_router
from app.api.v1.endpoints.compatibility import router as compatibility_router
from app.api.v1.endpoints.admin_endpoints import router as admin_router
from app.scheduler import scheduler
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError
import logging


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

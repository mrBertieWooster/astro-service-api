from app.api.v1.endpoints.horoscope import get_db
from app.db.database import Base
from app.main import app
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch
import logging

logger = logging.getLogger(__name__)

# Настройка тестовой базы данных
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="module")
async def test_db():
    """
    Создаёт асинхронное соединение с тестовой базой данных и предоставляет сессию.
    """
    logger.info("Initializing test database...")

    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},  # Необходимый параметр для SQLite
        future=True
    )

    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    testing_session_local = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with testing_session_local() as session:
        yield session
        
    logger.info("Tearing down test database...")

    # Очистка после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# Фикстура для тестирования API
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {
            "choices": [{"message": {"content": "Ваш гороскоп..."}}]
        }
        yield mock


@pytest.fixture
def mock_swiss_ephemeris():
    with patch("app.services.planet_calculation.calculate_planetary_positions") as mock:
        mock.return_value = {
            "sun": (120.0, 0.0, 1.0),  # (долгота, широта, расстояние)
            "moon": (45.0, 0.0, 1.0),
            "mercury": (90.0, 0.0, 1.0),
        }
        yield mock
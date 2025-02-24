from app.main import app
from app.db.database import get_db
from app.db.database import Base
from app.api.v1.models.user import City
from app.api.v1.models.zodiac import Zodiac 
from app.enums.zodiac import ZodiacElement, ZodiacQuality
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
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

    # **Создаём engine**
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True
    )

    # **Создаём таблицы**
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # **Создаём фабрику сессий**
    TestingSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # **Добавляем города и знаки зодиака**
    async with TestingSessionLocal() as session:
        # Проверяем, есть ли уже записи в БД
        existing_cities = await session.execute(select(City))
        existing_zodiacs = await session.execute(select(Zodiac))

        if not existing_cities.scalars().all():
            session.add_all([
                City(name="Москва", latitude=55.7558, longitude=37.6173),
                City(name="Таганрог", latitude=47.2362, longitude=38.8969),
                City(name="Санкт-Петербург", latitude=59.9343, longitude=30.3351),
            ])

        if not existing_zodiacs.scalars().all():
            session.add_all([
                Zodiac(name="aries", element=ZodiacElement.FIRE, ruling_planet="Марс", quality=ZodiacQuality.CARDINAL),
                Zodiac(name="taurus", element=ZodiacElement.EARTH, ruling_planet="Венера", quality=ZodiacQuality.FIXED),
                Zodiac(name="gemini", element=ZodiacElement.AIR, ruling_planet="Меркурий", quality=ZodiacQuality.MUTABLE),
                Zodiac(name="cancer", element=ZodiacElement.WATER, ruling_planet="Луна", quality=ZodiacQuality.CARDINAL),
                Zodiac(name="leo", element=ZodiacElement.FIRE, ruling_planet="Солнце", quality=ZodiacQuality.FIXED),
                Zodiac(name="virgo", element=ZodiacElement.EARTH, ruling_planet="Меркурий", quality=ZodiacQuality.MUTABLE),
                Zodiac(name="libra", element=ZodiacElement.AIR, ruling_planet="Венера", quality=ZodiacQuality.CARDINAL),
                Zodiac(name="scorpio", element=ZodiacElement.WATER, ruling_planet="Плутон", quality=ZodiacQuality.FIXED),
                Zodiac(name="sagittarius", element=ZodiacElement.FIRE, ruling_planet="Юпитер", quality=ZodiacQuality.MUTABLE),
                Zodiac(name="capricorn", element=ZodiacElement.EARTH, ruling_planet="Сатурн", quality=ZodiacQuality.CARDINAL),
                Zodiac(name="aquarius", element=ZodiacElement.AIR, ruling_planet="Уран", quality=ZodiacQuality.FIXED),
                Zodiac(name="pisces", element=ZodiacElement.WATER, ruling_planet="Нептун", quality=ZodiacQuality.MUTABLE),
            ])

        await session.commit()

    # **Переопределяем зависимость FastAPI для работы с тестовой БД**
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # **Передаём сессию в тесты**
    async with TestingSessionLocal() as session:
        yield session

    logger.info("Tearing down test database...")

    # **Удаляем зависимость**
    app.dependency_overrides.pop(get_db, None)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # **Закрываем engine**
    await engine.dispose()

# Фикстура для тестирования API
@pytest.fixture(scope="module")
def test_client():
    logger.info("Initializing test client...")
    with TestClient(app) as client:
        yield client
    logger.info("Tearing down test client...")

@pytest.fixture
async def mock_openai():
    with patch("openai.ChatCompletion.create") as mock:
        mock.return_value = {
            "choices": [{"message": {"content": "Ваш гороскоп..."}}]
        }
        yield mock


@pytest.fixture
def mock_swiss_ephemeris():
    with patch("app.services.planet_calculation.calculate_planetary_positions_and_houses") as mock:
        mock.return_value = {
            "sun": (120.0, 0.0, 1.0),  # (долгота, широта, расстояние)
            "moon": (45.0, 0.0, 1.0),
            "mercury": (90.0, 0.0, 1.0),
        }
        yield mock

        
@pytest.fixture
def mock_get_city_coordinates():
    with patch('app.services.geo.get_city_coordinates') as mock:
        mock.return_value = (55.7558, 37.6173)  # Москва, например
        yield mock
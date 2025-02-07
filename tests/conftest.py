from app.api.v1.endpoints.horoscope import get_db
from app.db.database import Base
from app.main import app
import pytest
from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from unittest.mock import patch

# Настройка тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def test_db():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, connect_args={"check_same_thread": False})
    connection = engine.connect()  # Создаём соединение
    transaction = connection.begin()  # Начинаем транзакцию
    Base.metadata.create_all(bind=Connection)
    session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, bind=connection)
    db = session()

    # Monkey-patch для эндпоинта
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield db
    
    transaction.rollback()
    Base.metadata.drop_all(bind=connection)
    connection.close()
    app.dependency_overrides.clear()

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
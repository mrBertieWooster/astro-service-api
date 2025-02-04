import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.api.v1.endpoints.horoscope import get_db

# Настройка тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Monkey-patch для эндпоинта
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)
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
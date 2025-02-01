import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.main import app
from fastapi.testclient import TestClient

# Настройка тестовой базы данных
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Фикстура для тестирования API
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
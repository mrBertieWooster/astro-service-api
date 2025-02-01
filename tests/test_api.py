from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_daily_horoscope():
    response = client.get("/horoscope/daily?sign=leo")
    assert response.status_code == 200
    assert "sign" in response.json()
    assert "prediction" in response.json()

def test_get_daily_horoscope_invalid_sign():
    response = client.get("/horoscope/daily?sign=invalid")
    assert response.status_code == 400
    assert "detail" in response.json()
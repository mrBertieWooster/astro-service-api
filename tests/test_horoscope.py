from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_horoscope():
    response = client.get("/api/v1/horoscope/aries")
    assert response.status_code == 200
    assert response.json()["zodiac_sign"] == "aries"
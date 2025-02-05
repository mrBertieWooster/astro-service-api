from app.api.v1.models.horoscope import Horoscope
from datetime import datetime, timedelta, timezone
import pytest

@pytest.mark.parametrize("sign", ["leo", "virgo", "aries"])
def test_get_daily_horoscope(test_db, test_client, sign):
    # Добавляем тестовые данные в базу
    utc_plus_3 = timezone(timedelta(hours=3))
    test_horoscope = Horoscope(sign=sign, prediction=f"Гороскоп для {sign}", date=datetime.now(utc_plus_3).date())
    test_db.add(test_horoscope)
    test_db.commit()
    
    assert test_db.query(Horoscope).filter(Horoscope.sign == sign).first() is not None

    # Вызов API
    response = test_client.get(f"/api/v1/horoscope/{sign}")
    
    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert "sign" in data
    assert "prediction" in data
    assert data["sign"] == sign
    assert data["prediction"] == f"Гороскоп для {sign}"

    test_db.rollback()


def test_get_daily_horoscope_invalid_sign(test_client):
    response = test_client.get("/api/v1/horoscope/invalid_sign")
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data
    
    errors = data["detail"]
    assert len(errors) == 1

    error = errors[0]
    assert error["loc"] == ["path", "zodiac_sign"]  # местоположение ошибки
    assert error["type"] == "enum"
    assert "Input should be 'aries', 'taurus'" in error["msg"]
from app.api.v1.models.horoscope import Horoscope
from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from unittest.mock import patch, AsyncMock
import pytest

@pytest.mark.parametrize("sign", ["leo", "virgo", "aries"])
@pytest.mark.asyncio
async def test_get_daily_horoscope(test_db, test_client, sign):
    """
    Тест получения ежедневного гороскопа.
    """
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()

    test_horoscope = Horoscope(
        sign=sign,
        prediction=f"Гороскоп для {sign}",
        date=current_date
    )
    test_db.add(test_horoscope)
    await test_db.commit()
    await test_db.refresh(test_horoscope)
    
    result = await test_db.execute(
        select(Horoscope).filter(
            Horoscope.sign == sign,
            Horoscope.date == current_date
        )
    )
    stored_horoscope = result.scalar_one_or_none()
    assert stored_horoscope is not None  # Проверяем, что запись существует

    response = test_client.post(
        f"/api/v1/horoscope/{sign}",
        json={
            "interval": "daily",
            "latitude": 55.7558,
            "longitude": 37.6173
        }
    )

    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert "sign" in data
    assert "prediction" in data
    assert data["sign"] == sign
    assert data["prediction"] == f"Гороскоп для {sign}"
    


def test_get_daily_horoscope_invalid_sign(test_client):
    response = test_client.post(
        f"/api/v1/horoscope/rhinoceros",
        json={
            "interval": "daily",
            "latitude": 55.7558,
            "longitude": 37.6173
        }
    )
    assert response.status_code == 422
    
    data = response.json()
    assert "detail" in data
    
    errors = data["detail"]
    assert len(errors) == 1

    error = errors[0]
    assert error["loc"] == ["path", "zodiac_sign"]  # местоположение ошибки
    assert error["type"] == "enum"
    assert "Input should be 'aries', 'taurus'" in error["msg"]
    
from app.api.v1.models.horoscope import Horoscope
from datetime import datetime, timedelta, timezone
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

    response = test_client.get(f"/api/v1/horoscope/{sign}")

    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert "sign" in data
    assert "prediction" in data
    assert data["sign"] == sign
    assert data["prediction"] == f"Гороскоп для {sign}"


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
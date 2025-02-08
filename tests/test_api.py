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

    response = test_client.get(f"/api/v1/horoscope/{sign}")

    # Проверки
    assert response.status_code == 200
    data = response.json()
    assert "sign" in data
    assert "prediction" in data
    assert data["sign"] == sign
    assert data["prediction"] == f"Гороскоп для {sign}"
    

@pytest.mark.asyncio
async def test_generate_new_horoscope(test_client):
    """
    Тест генерации нового гороскопа.
    """
    sign = "leo"
    utc_plus_3 = timezone(timedelta(hours=3))
    current_date = datetime.now(utc_plus_3).date()

    # Мокируем generate_horoscope_text
    with patch("app.services.horo_generator.generate_horoscope_text") as mock_generate:
        mock_generate.return_value = AsyncMock(return_value=f"Тестовый гороскоп для {sign}")

        # Вызов API
        response = test_client.get(f"/api/v1/horoscope/{sign}")

    # Проверки
    assert response.status_code == 200
    data = response.json()
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
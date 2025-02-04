from app.api.v1.models.horoscope import Horoscope
import pytest

@pytest.mark.parametrize("sign", ["leo", "virgo", "aries"])
def test_get_daily_horoscope(test_db, test_client, sign):
    # Добавляем тестовые данные в базу
    test_horoscope = Horoscope(sign=sign, prediction=f"Гороскоп для {sign}")
    test_db.add(test_horoscope)
    test_db.commit()

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
    response = test_client.get("/horoscope/daily?sign=invalid")
    assert response.status_code == 400
    assert "detail" in response.json()
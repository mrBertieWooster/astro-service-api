import pytest
from app.api.v1.models.user import User
from datetime import datetime

@pytest.mark.asyncio
async def test_check_user(test_client, test_db):
    
    date_of_birth = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
    time_of_birth = datetime.strptime("12:00:00", "%H:%M:%S").time()
    
    test_db.add(User(telegram_id="123456", name="Test User", date_of_birth=date_of_birth, time_of_birth=time_of_birth, city_id=1, sign_id=1, role="user"))
    await test_db.commit()

    response = test_client.get("/api/v1/user/123456")

    assert response.status_code == 200
    assert response.json() == {"exists": True}


@pytest.mark.asyncio
async def test_add_user(test_client, test_db):
    
    date_of_birth = datetime.strptime("1990-01-01", "%Y-%m-%d").date()
    time_of_birth = datetime.strptime("12:00:00", "%H:%M:%S").time()
    
    payload={
        "telegram_id": "654321",
        "name": "New User",
        "date_of_birth": date_of_birth.isoformat(),
        "time_of_birth": time_of_birth.isoformat()
    }
    
    response = test_client.post(
        "/api/v1/user/add",
        json=payload
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}

    response = test_client.get("/api/v1/user/654321")
    assert response.status_code == 200
    assert response.json() == {"exists": True}
    

@pytest.mark.asyncio
async def test_add_user_with_city(test_client, test_db, mock_get_city_coordinates):
    mock_get_city_coordinates.return_value = (55.7558, 37.6173)

    response = test_client.post(
        "/api/v1/user/add",
        json={
            "telegram_id": "1234567",
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "time_of_birth": "12:00:00",
            "city_name": "Москва"
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}


@pytest.mark.asyncio
async def test_add_user_with_zodiac(test_client, test_db, mock_get_city_coordinates):
    mock_get_city_coordinates.return_value = (55.7558, 37.6173) 

    response = test_client.post(
        "/api/v1/user/add",
        json={
            "telegram_id": "123457",
            "name": "Test User",
            "date_of_birth": "1990-01-01",
            "time_of_birth": "12:00:00",
            "city_name": "Москва"
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User added successfully"}

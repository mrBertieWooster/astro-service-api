from app.api.v1.models.zodiac import Zodiac
from app.api.v1.models.compatibility import Compatibility
from unittest.mock import AsyncMock, patch
import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_existing_compatibility(test_client, test_db):
    """
    Тест получения существующей совместимости.
    """
    
    logger.info(f'adding test data')
    
    zodiac1 = Zodiac(name="aries", element="fire", ruling_planet="Mars", quality="cardinal")
    zodiac2 = Zodiac(name="cancer", element="water", ruling_planet="Moon", quality="cardinal")
    test_db.add_all([zodiac1, zodiac2])
    await test_db.commit()
    await test_db.refresh(zodiac1)
    await test_db.refresh(zodiac2)

    compatibility = Compatibility(
        sign1_id=zodiac1.id,
        sign2_id=zodiac2.id,
        compatibility_percentage=40,
        description="Описание совместимости..."
    )
    test_db.add(compatibility)
    await test_db.commit()
    await test_db.refresh(compatibility)
    
    logger.info("Mocking OpenAI API call...")
    with patch("app.api.v1.endpoints.compatibility.generate_compatibility_description", new_callable=AsyncMock) as mock_generate:
        mock_generate.return_value = "Test compatibility description."

        logger.info("Calling API...")
        response = test_client.get("/api/v1/compatibility?sign1=aries&sign2=cancer")
        
    assert response.status_code == 200

    data = response.json()
    assert data["sign1"]["name"] == "aries"
    assert data["sign2"]["name"] == "cancer"
    assert data["compatibility_percentage"] == 40
    assert data["description"] == "Test compatibility description."
    
    mock_generate.assert_called_once_with("aries", "cancer")

    
""" @pytest.mark.asyncio
async def test_compatibility_openai_error(test_client, test_db):
    zodiac1 = Zodiac(name="aries", element="fire", ruling_planet="Mars", quality="cardinal")
    zodiac2 = Zodiac(name="cancer", element="water", ruling_planet="Moon", quality="cardinal")
    test_db.add_all([zodiac1, zodiac2])
    await test_db.commit()

    compatibility = Compatibility(
        sign1_id=zodiac1.id,
        sign2_id=zodiac2.id,
        compatibility_percentage=40,
        description=None  # Описание ещё не сгенерировано
    )
    test_db.add(compatibility)
    await test_db.commit()

    # Мокируем ошибку OpenAI
    with patch("app.services.zodiac_compatibility.generate_compatibility_description") as mock_generate:
        mock_generate.return_value = AsyncMock(side_effect=Exception("OpenAI error"))

        response = test_client.get("/api/v1/compatibility?sign1=aries&sign2=cancer")

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Не удалось сгенерировать описание совместимости." """

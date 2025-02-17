import pytest
from app.api.v1.models.tarot import TarotCard
from unittest.mock import AsyncMock, patch
from app.services.ai_clients.ai_clients import get_openai_client
import asyncio


@pytest.mark.asyncio
async def test_get_tarot_spread(test_client, test_db):
    # Добавляем тестовые карты в БД
    test_db.add(TarotCard(name="Шут", arcana="major", description="Описание", upright_meaning="Прямое значение", reversed_meaning="Перевернутое значение"))
    test_db.add(TarotCard(name="Маг", arcana="major", description="Описание", upright_meaning="Прямое значение", reversed_meaning="Перевернутое значение"))
    await test_db.commit()

    with patch("app.api.v1.endpoints.tarot.draw_tarot_cards", new_callable=AsyncMock) as MockDrawTarotCards, \
         patch("app.api.v1.endpoints.tarot.generate_tarot_interpretation", new_callable=AsyncMock) as MockInterpretation:
        
        MockInterpretation.return_value = "Мокированная интерпретация карт Таро"

        # Мокаем generate_tarot_interpretation
        MockDrawTarotCards.return_value = await asyncio.sleep(0, [
            {"name": "Шут", "position": "upright", "meaning": "Свобода"},
            {"name": "Маг", "position": "reversed", "meaning": "Манипуляция"}
        ])

        response = test_client.post(
            "/api/v1/tarot/spread",
            json={"spread_type": "card-of-the-day"}
        )

        assert response.status_code == 200
        data = response.json()
        
        mocked_cards = await MockDrawTarotCards()
        
        assert "cards" in data
        assert "interpretation" in data
        assert isinstance(mocked_cards, list)
        assert len(data["cards"]) == 2
        assert data["interpretation"] == "Мокированная интерпретация карт Таро"


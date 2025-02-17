from app.services.tarot_generator import draw_tarot_cards
from app.api.v1.models.tarot import TarotCard
from app.services.ai_clients.openai_client.taro_generation import generate_tarot_interpretation
from app.services.ai_clients.ai_clients import get_openai_client
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
import pytest


@pytest.mark.asyncio
async def test_generate_tarot_interpretation():
    with patch("app.services.ai_clients.openai_client.taro_generation.get_openai_client") as MockOpenAI:
        mock_client = AsyncMock()
        mock_client.chat.completions.create.return_value = AsyncMock(
            choices=[AsyncMock(message=AsyncMock(content="Твоя судьба связана с мудростью Таро!"))]
        )
        MockOpenAI.return_value = mock_client

        spread = [{"name": "Шут", "position": "upright", "meaning": "Свобода"}]
        spread_type = 'card-of-the-day'
        interpretation = await generate_tarot_interpretation(spread, spread_type)

        assert isinstance(interpretation, str)
        assert "Твоя судьба связана" in interpretation
        

@pytest.mark.asyncio
async def test_draw_tarot_cards(test_db: AsyncSession):
    # Добавляем тестовые карты
    test_db.add(TarotCard(name="Шут", arcana="major", description="Описание", upright_meaning="Прямое значение", reversed_meaning="Перевернутое значение"))
    test_db.add(TarotCard(name="Маг", arcana="major", description="Описание", upright_meaning="Прямое значение", reversed_meaning="Перевернутое значение"))
    await test_db.commit()

    cards = await draw_tarot_cards(test_db, 1)

    assert len(cards) == 1
    assert "name" in cards[0]
    assert "position" in cards[0]
    assert "meaning" in cards[0]
    
    

import pytest
from unittest.mock import patch, AsyncMock
from app.services.horo_generator import generate_horoscope_text

sign = "leo"
planetary_positions = {"sun": 120, "moon": 45, "mercury": 90}
aspects = [("sun", "moon", 120)]
houses = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
interval = 'день'


@pytest.mark.asyncio
async def test_generate_horoscope_text():
    """
    Тест генерации текста гороскопа через OpenAI.
    """
    sign = "leo"
    planetary_positions = {"sun": "Aries", "moon": "Taurus"}
    aspects = ["sun-moon: sextile"]
    interval = "день"

    # Мокируем асинхронный клиент OpenAI
    with patch("app.services.ai_clients.openai_client.apenai_horo_generation.AsyncOpenAI") as MockOpenAI:
        mock_client = MockOpenAI.return_value

        # Создаём моковый ответ
        mock_message = AsyncMock()
        mock_message.content = "Ваш гороскоп..."

        mock_choice = AsyncMock()
        mock_choice.message = mock_message

        mock_response = AsyncMock()
        mock_response.choices = [mock_choice]

        # Настраиваем мок для асинхронного метода create
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        # Вызываем тестируемую функцию
        prediction = await generate_horoscope_text(sign, planetary_positions, aspects, interval)

    # Проверки
    assert isinstance(prediction, str)
    assert len(prediction) > 0
    assert prediction == "Ваш гороскоп..."

    expected_content = (
        f"Составь гороскоп для знака {sign} на основе следующих данных:\n"
        f"Положения планет и дома: {planetary_positions}\n"
        f"Аспекты: {aspects}\n"
        f"Гороскоп должен быть составлен на {interval}"
    )

    # Проверяем, что мок был вызван с правильными параметрами
    mock_client.chat.completions.create.assert_awaited_once_with(
        model="gpt-4o",
        messages=[{"role": "user", "content": expected_content}],
        max_tokens=2000,
        timeout=30
    )

"""
@patch("app.services.ai_clients.openai_client.apenai_horo_generation.AsyncOpenAI")  
async def test_generate_horoscope_text_openai_error(mock_openai):
    mock_instance = mock_openai.return_value  # Создаём мокнутый экземпляр OpenAI
    mock_instance.chat.completions.create.side_effect = RuntimeError("OpenAI API error")

    try:
        prediction = await generate_horoscope_text("leo", {}, [], [])
    except Exception as e:
        pytest.fail(f"Функция не обработала ошибку OpenAI: {e}")

    assert "OpenAI API error" in prediction.lower()
""" 
  
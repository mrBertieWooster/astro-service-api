from unittest.mock import patch, Mock
from app.services.horo_generator import generate_horoscope_text

sign = "leo"
planetary_positions = {"sun": 120, "moon": 45, "mercury": 90}
aspects = [("sun", "moon", 120)]
houses = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
interval = 'день'


@patch("app.services.ai_clients.openai_client.apenai_horo_generation.OpenAI")
def test_generate_horoscope_text(mock_openai):
    mock_client = mock_openai.return_value
    
    # мок для OpenAI
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Ваш гороскоп..."))]
    
    # Настраиваем мок для метода create
    mock_client.chat.completions.create.return_value = mock_response

    prediction = generate_horoscope_text(sign, planetary_positions, aspects, houses, interval)
    
    # Проверки
    assert isinstance(prediction, str)
    assert len(prediction) > 0
    assert prediction == "Ваш гороскоп..."

    # Проверка, что мок был вызван с правильными параметрами
    mock_client.chat.completions.create.assert_called_once()

def test_generate_horoscope_text_openai_error(mock_openai):
    mock_openai.side_effect = Exception("OpenAI API error")
    prediction = generate_horoscope_text(sign, planetary_positions, aspects, houses, interval)
    assert "не удалось сгенерировать гороскоп" in prediction.lower()  # Проверяем, что ошибка обрабатывается
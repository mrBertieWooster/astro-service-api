from app.services.horo_generator import generate_horoscope_text

def test_generate_horoscope_text(mock_openai):
    sign = "leo"
    aspects = [("sun", "moon", 120)]  # Пример аспектов
    houses = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]  # Пример домов
    prediction = generate_horoscope_text(sign, aspects, houses)
    assert isinstance(prediction, str)
    assert len(prediction) > 0

def test_generate_horoscope_text_openai_error(mock_openai):
    mock_openai.side_effect = Exception("OpenAI API error")
    sign = "leo"
    aspects = [("sun", "moon", 120)]
    houses = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    prediction = generate_horoscope_text(sign, aspects, houses)
    assert "ошибка" in prediction.lower()  # Проверяем, что ошибка обрабатывается
from app.services.horo_generator import generate_horoscope_text

def test_generate_horoscope_text():
    sign = "leo"
    planetary_positions = {"sun": 120, "moon": 45, "mercury": 90}
    prediction = generate_horoscope_text(sign, planetary_positions)
    
    # Проверяем, что возвращается строка
    assert isinstance(prediction, str)
    assert len(prediction) > 0
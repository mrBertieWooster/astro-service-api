from datetime import datetime
from app.services.planet_calculation import calculate_planetary_positions_and_houses, calculate_aspects

def test_calculate_planetary_positions(mock_swiss_ephemeris):
    date = datetime(2023, 10, 10)
    positions = calculate_planetary_positions_and_houses(date)
    
    # Проверяем, что возвращается словарь с корректными разделами
    assert isinstance(positions, dict)
    assert "planets" in positions
    assert "houses" in positions
    assert "ascendant" in positions
    assert "midheaven" in positions

    # Проверяем, что в разделе "planets" есть ключи с позициями
    assert "sun" in positions["planets"]
    assert "moon" in positions["planets"]

    # Проверяем, что данные планет представляют собой словари
    assert isinstance(positions["planets"]["sun"], dict)
    assert isinstance(positions["planets"]["moon"], dict)

    # Проверяем наличие долготы, широты и дистанции у Солнца
    assert "longitude" in positions["planets"]["sun"]
    assert "latitude" in positions["planets"]["sun"]
    assert "distance" in positions["planets"]["sun"]

def test_calculate_aspects(mock_swiss_ephemeris):
    date = datetime(2023, 10, 10)
    positions = calculate_planetary_positions_and_houses(date)

    # Передаем только координаты планет
    aspects = calculate_aspects(positions["planets"])

    # Проверяем, что возвращается список аспектов
    assert isinstance(aspects, list)
    for aspect in aspects:
        assert len(aspect) == 3  # (планета1, планета2, угол)
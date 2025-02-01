from datetime import datetime
from app.services.planet_calculation import calculate_planetary_positions, calculate_aspects

def test_calculate_planetary_positions():
    date = datetime(2023, 10, 10)
    positions = calculate_planetary_positions(date)
    
    # Проверяем, что возвращается словарь с позициями планет
    assert isinstance(positions, dict)
    assert "sun" in positions
    assert "moon" in positions
    assert isinstance(positions["sun"], tuple)

def test_calculate_aspects():
    date = datetime(2023, 10, 10)
    positions = calculate_planetary_positions(date)
    aspects = calculate_aspects(positions)
    
    # Проверяем, что возвращается список аспектов
    assert isinstance(aspects, list)
    for aspect in aspects:
        assert len(aspect) == 3  # (планета1, планета2, угол)
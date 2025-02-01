from datetime import datetime
from app.services.planet_calculation import calculate_planetary_positions

def test_calculate_planetary_positions():
    date = datetime(2023, 10, 10)
    positions = calculate_planetary_positions(date)
    assert 'sun' in positions
    assert 'moon' in positions
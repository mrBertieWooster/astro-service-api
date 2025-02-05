from app.config import settings
import swisseph as swe
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

swe.set_ephe_path(settings.EPHEMERIS_PATH)

def calculate_planetary_positions(date: datetime):
    """
    Рассчитывает положения планет на указанную дату.
    Возвращает словарь с позициями планет.
    """
    logger.debug(f'calculating planetary positions')
    
    jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)
    planets = {
        'sun': swe.SUN,
        'moon': swe.MOON,
        'mercury': swe.MERCURY,
        'venus': swe.VENUS,
        'mars': swe.MARS,
        'jupiter': swe.JUPITER,
        'saturn': swe.SATURN,
        'uranus': swe.URANUS,
        'neptune': swe.NEPTUNE,
        'pluto': swe.PLUTO,
    }
    positions = {}
    for name, planet in planets.items():
        positions[name] = swe.calc_ut(jd, planet)[0]  # Положение планеты (долгота)
    return positions

def calculate_aspects(planetary_positions):
    """
    Рассчитывает аспекты между планетами.
    Возвращает список аспектов в формате (планета1, планета2, угол).
    """
    aspects = []
    planets = list(planetary_positions.keys())
    
    for i in range(len(planets)):
        for j in range(i + 1, len(planets)):
            planet1 = planets[i]
            planet2 = planets[j]
            
            # Извлекаем долготу обеих планет
            lon1 = planetary_positions[planet1][0]
            lon2 = planetary_positions[planet2][0]
            
            # Вычисляем угол между планетами
            angle = abs(lon1 - lon2)
            if angle > 180:
                angle = 360 - angle
            
            aspects.append((planet1, planet2, angle))
    
    return aspects

def calculate_houses(date: datetime, lat: float, lon: float):
    """
    Рассчитывает дома гороскопа для указанной даты и места.
    Возвращает позиции куспидов домов.
    """
    jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)
    houses = swe.houses(jd, lat, lon, b'P')  # Система Плацидуса
    return houses[0]  # Куспиды домов
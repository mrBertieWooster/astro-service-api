from app.config import settings
from app.exceptions import CalculatingPlanetsError
import swisseph as swe
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

swe.set_ephe_path(settings.EPHEMERIS_PATH)


def determine_sign(longitude: float) -> str:
    """
    Определяет знак зодиака на основе долготы планеты.
    
    :param longitude: Долгота планеты в градусах (0° - 360°).
    :return: Название знака зодиака.
    """
    zodiac_signs = [
        "aries", "taurus", "gemini", "cancer", "leo", "virgo",
        "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
    ]
    
    index = int(longitude // 30)
    
    return zodiac_signs[index]

def calculate_houses(jd: float, latitude: float, longitude: float, house_system: bytes = b'P'):
    """
    Рассчитывает куспиды домов гороскопа и асцендент.
    
    :param jd: Юлианская дата
    :param latitude: широта места
    :param longitude: долгота места
    :param house_system: система домов ('P' - Плацидус, 'K' - Кох и т.д.)
    :return: (список из 12 куспидов домов, асцендент, MC)
    """
    try:
        houses, ascmc = swe.houses(jd, latitude, longitude, house_system)

        # Асцендент (ASC) и Среднее небо (MC)
        asc = ascmc[0]  # Асцендент (1-й дом)
        mc = ascmc[1]   # Среднее небо (10-й дом)

        return houses, asc, mc
    except CalculatingPlanetsError as e:
        logger.error(f'Error while calculating houses: {str(e)}')
        raise


def determine_house_from_position(planet_longitude: float, houses: list):
    """
    Определяет, в каком доме находится планета, исходя из ее долготы и куспидов домов.
    
    :param planet_longitude: Долгота планеты.
    :param houses: Список куспидов домов.
    :return: Номер дома (1-12).
    """
    try:
        for i in range(12):
            if houses[i] <= planet_longitude < houses[(i + 1) % 12]:
                return i + 1  # Дома нумеруются с 1 до 12
        return 12  # Если не найдено, возвращаем 12-й дом по умолчанию
    
    except CalculatingPlanetsError as e:
        logger.error(f'Error while determinig houses from positions: {str(e)}')
        raise


def calculate_planetary_positions_and_houses(
    date: datetime,
    time_of_birth: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    logger.debug('Calculating planetary positions and houses')

    # Учитываем время рождения, если оно передано
    try:
        if time_of_birth:
            hours, minutes, *rest = map(int, time_of_birth.split(":"))
            date = datetime.strptime(date, "%d.%m.%Y")
            date = date.replace(hour=hours, minute=minutes)

        # Рассчитываем юлианскую дату (UTC)
        jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)

        # Система домов Плацидуса (если координаты указаны)
        houses, asc, mc = calculate_houses(jd, latitude, longitude) if latitude and longitude else (None, None, None)

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

        planetary_positions = {}
        for name, planet in planets.items():
            
            position_data, _ = swe.calc_ut(jd, planet)
            lon, lat, dist, _, _, _ = position_data # только координаты и расстояние
            
            # созвездие, в котором планета
            sign = determine_sign(lon)
            
            # дом планеты
            house = determine_house_from_position(lon, houses) if houses else None
            
            planetary_positions[name] = {
                "longitude": lon,
                "latitude": lat,
                "distance": dist,
                "sign": sign,
                "house": house
            }

        logger.info(f"Calculated planetary positions and houses: {planetary_positions}")
        
        return {
            "planets": planetary_positions,
            "houses": {str(i + 1): house for i, house in enumerate(houses)} if houses else {},
            "ascendant": asc if asc is not None else 0.0, #асцендент
            "midheaven": mc if mc is not None else 0.0 #MC (среднее небо)   
        }
    
    except CalculatingPlanetsError as e:
        logger.error(f'Error while planetary positions: {str(e)}')
        raise


def calculate_aspects(planetary_positions):
    """
    Рассчитывает аспекты между планетами.
    Возвращает список аспектов в формате (планета1, планета2, угол).
    """
    aspects = []
    planets = list(planetary_positions.keys())  # Теперь это только список планет
    
    try:
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]

                # Извлекаем долготу обеих планет
                lon1 = planetary_positions[planet1]["longitude"]  # Исправлено  longitude
                lon2 = planetary_positions[planet2]["longitude"]

                # Вычисляем угол между планетами
                angle = abs(lon1 - lon2)
                if angle > 180:
                    angle = 360 - angle

                aspects.append((planet1, planet2, angle))

        return aspects
    except CalculatingPlanetsError as e:
        logger.error(f'Error while calculating aspects: {str(e)}')
        raise
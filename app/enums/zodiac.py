from enum import Enum

class ZodiacSign(str, Enum):
    ARIES = "aries"
    TAURUS = "taurus"
    GEMINI = "gemini"
    CANCER = "cancer"
    LEO = "leo"
    VIRGO = "virgo"
    LIBRA = "libra"
    SCORPIO = "scorpio"
    SAGITTARIUS = "sagittarius"
    CAPRICORN = "capricorn"
    AQUARIUS = "aquarius"
    PISCES = "pisces"
    

class IntervalType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    
class ZodiacElement(str, Enum):
    """
    Стихии знаков зодиака.
    """
    FIRE = "fire"
    WATER = "water"
    EARTH = "earth"
    AIR = "air"
    
class ZodiacQuality(str, Enum):
    """
    Качества знаков зодиака.
    """
    CARDINAL = "cardinal"   # Кардинальные
    FIXED = "fixed"         # Фиксированные
    MUTABLE = "mutable"     # Мутабельные (Переменные)
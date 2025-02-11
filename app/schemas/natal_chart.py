from pydantic import BaseModel
from typing import List, Dict

class PlaceOfBirth(BaseModel):
    latitude: float
    longitude: float

class NatalChartRequest(BaseModel):
    date_of_birth: str  # "YYYY-MM-DD"
    time_of_birth: str  # "HH:MM:SS"
    place_of_birth: PlaceOfBirth

class PlanetPosition(BaseModel):
    sign: str
    house: int

class Aspect(BaseModel):
    planet1: str
    planet2: str
    aspect: str
    degree: float

class House(BaseModel):
    ruler: str
    occupied_by: List[str]

class NatalChartResponse(BaseModel):
    description: str
    planets: Dict[str, PlanetPosition]
    aspects: List[Aspect]
    houses: Dict[int, House]

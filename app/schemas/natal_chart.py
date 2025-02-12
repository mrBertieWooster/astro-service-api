from pydantic import BaseModel, Field
from typing import List, Dict, Tuple, Any

class PlaceOfBirth(BaseModel):
    latitude: float
    longitude: float

class NatalChartRequest(BaseModel):
    date_of_birth: str  # "DD.MM.YYYY"
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
    description: str = Field(..., description="Готовое текстовое описание натальной карты.")
    planets: Dict[str, Any] = Field(..., description="Положения планет, включая знаки и дома.")
    aspects: List[Tuple[str, str, float]] = Field(..., description="Список аспектов между планетами.")

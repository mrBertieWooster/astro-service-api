from pydantic import BaseModel, Field
from typing import List, Dict, Any

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
    description: str = Field(..., description="Готовое текстовое описание натальной карты.")
    planets: Dict[str, Dict[str, Any]] = Field(..., description="Положения планет, включая знаки и дома.")
    aspects: List[Dict[str, Any]] = Field(..., description="Список аспектов между планетами.")
    houses: Dict[int, float] = Field(..., description="Долготы куспидов домов.")
    ascendant: float = Field(..., ge=0, le=360, description="Асцендент в градусах эклиптической долготы.")
    midheaven: float = Field(..., ge=0, le=360, description="Средина Неба (MC) в градусах эклиптической долготы.")

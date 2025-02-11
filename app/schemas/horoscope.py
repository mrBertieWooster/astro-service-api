from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.enums.zodiac import ZodiacSign, IntervalType

class HoroscopeRequestSchema(BaseModel):
    interval: IntervalType = Field("daily", description="Интервал гороскопа (daily, weekly, monthly)")
    latitude: Optional[float] = Field(None, description="Широта места (например, 55.75)")
    longitude: Optional[float] = Field(None, description="Долгота места (например, 37.61)")

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, value: str) -> str:
        allowed_intervals = {"daily", "weekly", "monthly"}
        if value not in allowed_intervals:
            raise ValueError("Интервал должен быть одним из: daily, weekly, monthly")
        return value

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def validate_coordinates(cls, value: Optional[float], info) -> Optional[float]:
        if value is not None:
            field_name = info.field_name
            if field_name == "latitude" and (value < -90 or value > 90):
                raise ValueError("Широта должна быть в диапазоне от -90 до 90 градусов.")
            if field_name == "longitude" and (value < -180 or value > 180):
                raise ValueError("Долгота должна быть в диапазоне от -180 до 180 градусов.")
        return value

class PlanetPosition(BaseModel):
    planet: str
    position: float
    
class HoroscopeResponse(BaseModel):
    sign: str
    prediction: str
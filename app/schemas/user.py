from pydantic import BaseModel, Field
from typing import Optional

class CitySchema(BaseModel):
    name: str = Field(..., description="Название города")
    latitude: float = Field(..., description="Широта города")
    longitude: float = Field(..., description="Долгота города")

class UserCreateRequest(BaseModel):
    telegram_id: str
    name: str
    date_of_birth: Optional[str] = None  # YYYY-MM-DD
    time_of_birth: Optional[str] = None  # HH:MM:SS
    city_name: Optional[str] = None  # Название города, если не передано - Москва

class UserResponse(BaseModel):
    exists: bool

class UserDetailResponse(BaseModel):
    telegram_id: str
    name: str
    date_of_birth: Optional[str]
    time_of_birth: Optional[str]
    city: str
    sign: str
    role: str

from pydantic import BaseModel, Field
from typing import Optional
from typing import List

class PlaceOfBirth(BaseModel):
    latitude: float = Field(..., description="Широта места рождения")
    longitude: float = Field(..., description="Долгота места рождения")

class PersonData(BaseModel):
    name: Optional[str] = Field(None, description="Имя человека")
    date_of_birth: str = Field(..., description="Дата рождения в формате YYYY-MM-DD")
    time_of_birth: Optional[str] = Field(None, description="Время рождения в формате HH:MM")
    place_of_birth: PlaceOfBirth = Field(..., description="Место рождения")

class CompatibilityRequest(BaseModel):
    first_person: PersonData
    second_person: PersonData

class CompatibilityAspect(BaseModel):
    planet_1: str
    planet_2: str
    aspect: str

class CompatibilityResponse(BaseModel):
    first_person_sign: str
    second_person_sign: str
    compatibility_score: int = Field(..., ge=0, le=100, description="Процент совместимости от 0 до 100")
    compatibility_text: str
    aspects: List[CompatibilityAspect]

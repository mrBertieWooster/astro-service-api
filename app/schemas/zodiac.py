from pydantic import BaseModel, ConfigDict
from typing import Optional

class ZodiacInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    element: str
    ruling_planet: str
    quality: str

class ZodiacCompatibilityResponse(BaseModel):
    sign1: ZodiacInfo
    sign2: ZodiacInfo
    compatibility_percentage: int
    description: Optional[str]
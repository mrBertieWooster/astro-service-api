from sqlalchemy import Column, String, Integer, Enum
from app.db.database import Base
from app.enums.zodiac import ZodiacElement, ZodiacQuality

class Zodiac(Base):
    __tablename__ = "zodiacs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False) 
    element = Column(Enum(ZodiacElement), nullable=False)  # Стихия
    ruling_planet = Column(String, nullable=False)  # Планета
    quality = Column(Enum(ZodiacQuality), nullable=False)  # Качество
    

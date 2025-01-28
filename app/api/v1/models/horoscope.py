from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Horoscope(Base):
    __tablename__ = "horoscopes"

    id = Column(Integer, primary_key=True, index=True)
    zodiac_sign = Column(String, unique=True, index=True)
    prediction = Column(String)
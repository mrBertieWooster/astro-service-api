from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class TarotCard(Base):
    __tablename__ = "tarot_cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    arcana = Column(String, nullable=False)  # 'major' или 'minor'
    suit = Column(String, nullable=True)  # 'кубки', 'жезлы', 'мечи', 'пентакли' (только для minor)
    description = Column(Text, nullable=False)
    upright_meaning = Column(Text, nullable=False)
    reversed_meaning = Column(Text, nullable=False)
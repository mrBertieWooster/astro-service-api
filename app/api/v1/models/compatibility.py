from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
    
class Compatibility(Base):
    __tablename__ = "compatibilities"

    id = Column(Integer, primary_key=True, index=True)
    sign1_id = Column(Integer, ForeignKey("zodiacs.id"), nullable=False)  # Первый знак
    sign2_id = Column(Integer, ForeignKey("zodiacs.id"), nullable=False)  # Второй знак
    compatibility_percentage = Column(Integer, nullable=False)  # Процент совместимости
    description = Column(String, nullable=True)  # Уникальное описание совместимости

    # Отношения с таблицей Zodiac
    sign1 = relationship("Zodiac", foreign_keys=[sign1_id])
    sign2 = relationship("Zodiac", foreign_keys=[sign2_id])
    
    

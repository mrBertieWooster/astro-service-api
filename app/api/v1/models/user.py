from app.db.database import Base
from sqlalchemy import Column, Integer, Float, String, Date, Time, ForeignKey, Enum
from sqlalchemy.orm import relationship


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    time_of_birth = Column(Time, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False, default=1)  # По умолчанию Москва
    
    city = relationship("City")
    
    sign_id = Column(Integer, ForeignKey("zodiacs.id"), nullable=True)  # Ссылка на знак зодиака
    sign = relationship("Zodiac")

    role = Column(Enum("admin", "user", name="user_role_enum"), default=UserRole.USER, nullable=False)
    
    
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

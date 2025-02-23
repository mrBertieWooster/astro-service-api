from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

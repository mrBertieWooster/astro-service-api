from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from app.db.database import Base

utc_plus_3 = timezone(timedelta(hours=3))

class Horoscope(Base):
    __tablename__ = 'horoscopes'

    id = Column(Integer, primary_key=True, index=True)
    sign = Column(String, index=True)  # Знак зодиака
    prediction = Column(String)  # Текст гороскопа
    date = Column(Date, index=True)  # Дата гороскопа
    type = Column(String, index=True, default='daily')  # Тип гороскопа (daily, weekly, love и т.д.)
    created_at = Column(DateTime, default=datetime.now(utc_plus_3))  # Время создания
    updated_at = Column(DateTime, default=datetime.now(utc_plus_3), onupdate=datetime.now(utc_plus_3))  # Время обновления
    language = Column(String, default='ru')  # Язык гороскопа
    source = Column(String, default='swisseph')  # Источник данных
    is_active = Column(Boolean, default=True)  # Активен ли гороскоп
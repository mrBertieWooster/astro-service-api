from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone


class Base(DeclarativeBase):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now, nullable=False)

def get_db_url():
    return settings.DATABASE_URL

def create_engine():
    return create_async_engine(
        get_db_url(),
        future=True, 
        echo=settings.DEBUG
    )

def create_session_factory(engine):
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


engine = create_engine()
async_session = create_session_factory(engine)


async def get_db():
    """
    Dependency для FastAPI: создаёт и возвращает асинхронную сессию.
    """
    async with async_session() as session:
        yield session
        await session.close()

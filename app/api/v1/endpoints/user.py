from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import get_db
from app.api.v1.models.user import User, City
from app.schemas.user import UserCreateRequest, UserDetailResponse
from app.services.geo import get_city_coordinates
from app.services.astro_utils import get_zodiac_sign
from app.config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{user_id}", response_model=UserDetailResponse)
async def check_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """
    Проверяет, существует ли пользователь в базе данных и отдает его данные.
    """
    
    logger.info(f"Session state before query: {db.is_active}")
    
    result = await db.execute(
            select(User).filter(User.telegram_id == user_id).options(
                selectinload(User.city),
                selectinload(User.sign)
            )
        )
    
    logger.info(f"Session state after query: {db.is_active}")
    
    user = result.scalars().first()
    
    if not user:
        return {"exists": False}
    
    return UserDetailResponse(
            telegram_id=user.telegram_id,
            name=user.name,
            date_of_birth=user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
            time_of_birth=user.time_of_birth.strftime("%H:%M:%S") if user.time_of_birth else None,
            city=user.city.name,
            sign=user.sign.name,
            role=user.role
        )


@router.post("/add")
async def add_user(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Добавляет нового пользователя в базу данных.
    Если город не найден, добавляет его в базу перед записью пользователя.
    """
    try:
        # Проверяем, есть ли пользователь
        
        logger.info(f"Session state before query: {db.is_active}")
        
        result = await db.execute(select(User).filter(User.telegram_id == user_data.telegram_id))
        existing_user = result.scalar()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        logger.info(f"Session state after query: {db.is_active}")

        # Определяем город пользователя
        city_name = user_data.city_name or settings.DEFAULT_CITY
        city_result = await db.execute(select(City).filter(City.name == city_name))
        city = city_result.scalar_one_or_none()

        if not city:
            latitude, longitude = get_city_coordinates(city_name)
            if latitude is None or longitude is None:
                raise HTTPException(status_code=400, detail="City coordinates not found")

            city = City(name=city_name, latitude=latitude, longitude=longitude)
            db.add(city)
            await db.flush()

        sign_id = None
        if user_data.date_of_birth:
            sign_id = await get_zodiac_sign(db, user_data.date_of_birth)
            
        
        date_of_birth = datetime.strptime(user_data.date_of_birth, "%Y-%m-%d").date()
        time_of_birth = datetime.strptime(user_data.time_of_birth, "%H:%M:%S").time()

        # Создаем нового пользователя
        new_user = User(
            telegram_id=user_data.telegram_id,
            name=user_data.name,
            date_of_birth=date_of_birth,
            time_of_birth=time_of_birth,
            city_id=city.id,
            sign_id=sign_id,
            role="user"
        )
        db.add(new_user)
        await db.commit()
        
        return {"message": "User added successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f'Database error: {str(e)}')
        raise
    except Exception as e:
        logger.error(f'Failed to add user: {str(e)}')
        raise

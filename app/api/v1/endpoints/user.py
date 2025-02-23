from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import get_db
from app.api.v1.models.user import User
from app.schemas.user import UserCreateRequest, UserResponse

router = APIRouter()

@router.get("/{user_id}", response_model=UserResponse)
async def check_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """
    Проверяет, существует ли пользователь в базе данных.
    """
    result = await db.execute(select(User).filter(User.telegram_id == user_id))
    user = result.scalar_one_or_none()
    return {"exists": user is not None}

@router.post("/add")
async def add_user(user_data: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    Добавляет нового пользователя в базу данных.
    """
    # Проверяем, есть ли уже такой пользователь
    existing_user = await db.execute(select(User).filter(User.telegram_id == user_data.telegram_id))
    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    # Создаем нового пользователя
    new_user = User(telegram_id=user_data.telegram_id, name=user_data.name)
    db.add(new_user)
    await db.commit()
    return {"message": "User added successfully"}

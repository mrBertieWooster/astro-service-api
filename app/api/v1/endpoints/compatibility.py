from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import get_db
from app.api.v1.models.zodiac import Zodiac
from app.api.v1.models.compatibility import Compatibility
from app.services.compatibility import generate_compatibility_description
from app.schemas.zodiac import ZodiacCompatibilityResponse, ZodiacInfo
from app.enums.zodiac import ZodiacSign
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", summary="Проверить совместимость двух знаков зодиака")
async def check_zodiac_compatibility(
    sign1: ZodiacSign,
    sign2: ZodiacSign,
    db: AsyncSession = Depends(get_db)
) -> ZodiacCompatibilityResponse:
    """
    Проверяет совместимость между двумя знаками зодиака.
    """
    try:
        
        logger.info(f'checking signs')
        
        if sign1 == sign2:
            zodiac_info = await db.execute(select(Zodiac).where(Zodiac.name == sign1.value))
            zodiac = zodiac_info.scalar_one_or_none()
            
            logger.info(f'got zodiac {zodiac}')

            if not zodiac:
                raise HTTPException(status_code=404, detail=f"Знак {sign1.value} не найден")

            return ZodiacCompatibilityResponse(
                sign1=zodiac,
                sign2=zodiac,
                compatibility_percentage=100,
                description=f"{sign1.value.capitalize()} полностью совместим с самим собой."
            )

        
        zodiac1_info = await db.execute(select(Zodiac).where(Zodiac.name == sign1.value))
        logger.info(f'the first sign {zodiac1_info}')
        
        zodiac2_info = await db.execute(select(Zodiac).where(Zodiac.name == sign2.value))
        logger.info(f'the second sign {zodiac2_info}')

        zodiac1 = zodiac1_info.scalar_one_or_none()
        zodiac2 = zodiac2_info.scalar_one_or_none()

        if not zodiac1 or not zodiac2:
            raise HTTPException(status_code=404, detail="Один из знаков не найден")

        # Получаем совместимость из БД
        compatibility_info = await db.execute(
            select(Compatibility).where(
                (Compatibility.sign1_id == zodiac1.id) & (Compatibility.sign2_id == zodiac2.id) |
                (Compatibility.sign1_id == zodiac2.id) & (Compatibility.sign2_id == zodiac1.id)
            )
        )
        compatibility = compatibility_info.scalar_one_or_none()

        if not compatibility:
            raise HTTPException(status_code=404, detail="Не найдено соответствие между знаками")
        
        description = await generate_compatibility_description(sign1.value, sign2.value)

        # Формируем ответ
        return ZodiacCompatibilityResponse(
            sign1=ZodiacInfo.model_validate(zodiac1),
            sign2=ZodiacInfo.model_validate(zodiac2),
            compatibility_percentage=compatibility.compatibility_percentage,
            description=description
        )
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")
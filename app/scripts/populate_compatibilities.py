from app.api.v1.models.zodiac import Zodiac
from app.api.v1.models.compatibility import Compatibility
from app.enums.zodiac import ZodiacElement, ZodiacQuality
from app.db.database import async_session
from sqlalchemy.future import select
import asyncio
import logging

logger = logging.getLogger("astro-service-api")

async def populate_compatibilities():
    """
    Заполняет таблицу compatibilities базовыми значениями совместимости.
    """
    async with async_session() as db:
        try:
            zodiacs = (await db.execute(select(Zodiac))).scalars().all()

            if not zodiacs:
                raise ValueError("No zodiacs found in the database.")

            for i, zodiac1 in enumerate(zodiacs):
                for j, zodiac2 in enumerate(zodiacs):
                    if i <= j:  # Избегаем дублирования пар
                        compatibility = Compatibility(
                            sign1_id=zodiac1.id,
                            sign2_id=zodiac2.id,
                            compatibility_percentage=calculate_base_compatibility(zodiac1.element, zodiac2.element),
                            description=None  # Описание будет генерироваться позже
                        )
                        db.add(compatibility)

            await db.commit()
            logger.info("Compatibilities table populated successfully.")
        except Exception as e:
            logger.error(f"Failed to populate compatibilities table: {str(e)}")
            await db.rollback()

def calculate_base_compatibility(element1: ZodiacElement, element2: ZodiacElement) -> int:
    """
    Рассчитывает базовый процент совместимости между элементами.
    """
    base_compatibility = {
        ("fire", "fire"): 80,
        ("fire", "water"): 40,
        ("fire", "earth"): 30,
        ("fire", "air"): 60,
        ("water", "water"): 70,
        ("water", "earth"): 50,
        ("water", "air"): 30,
        ("earth", "earth"): 80,
        ("earth", "air"): 40,
        ("air", "air"): 70,
    }

    key = tuple(sorted([element1.value, element2.value]))
    return base_compatibility.get(key, 50)  # По умолчанию 50%

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(populate_compatibilities())
from app.api.v1.models.zodiac import Zodiac
from app.db.database import async_session
from app.enums.zodiac import ZodiacElement, ZodiacQuality
import asyncio
import logging

logger = logging.getLogger(__name__)

async def populate_zodiacs():
    """
    Заполняет таблицу zodiacs данными о знаках зодиака.
    """
    zodiac_data = [
        {"name": "aries", "element": ZodiacElement.FIRE, "ruling_planet": "Mars", "quality": ZodiacQuality.CARDINAL},
        {"name": "taurus", "element": ZodiacElement.EARTH, "ruling_planet": "Venus", "quality": ZodiacQuality.FIXED},
        {"name": "gemini", "element": ZodiacElement.AIR, "ruling_planet": "Mercury", "quality": ZodiacQuality.MUTABLE},
        {"name": "cancer", "element": ZodiacElement.WATER, "ruling_planet": "Moon", "quality": ZodiacQuality.CARDINAL},
        {"name": "leo", "element": ZodiacElement.FIRE, "ruling_planet": "Sun", "quality": ZodiacQuality.FIXED},
        {"name": "virgo", "element": ZodiacElement.EARTH, "ruling_planet": "Mercury", "quality": ZodiacQuality.MUTABLE},
        {"name": "libra", "element": ZodiacElement.AIR, "ruling_planet": "Venus", "quality": ZodiacQuality.CARDINAL},
        {"name": "scorpio", "element": ZodiacElement.WATER, "ruling_planet": "Pluto", "quality": ZodiacQuality.FIXED},
        {"name": "sagittarius", "element": ZodiacElement.FIRE, "ruling_planet": "Jupiter", "quality": ZodiacQuality.MUTABLE},
        {"name": "capricorn", "element": ZodiacElement.EARTH, "ruling_planet": "Saturn", "quality": ZodiacQuality.CARDINAL},
        {"name": "aquarius", "element": ZodiacElement.AIR, "ruling_planet": "Uranus", "quality": ZodiacQuality.FIXED},
        {"name": "pisces", "element": ZodiacElement.WATER, "ruling_planet": "Neptune", "quality": ZodiacQuality.MUTABLE},
    ]

    async with async_session() as db:
        try:
            for data in zodiac_data:
                zodiac = Zodiac(**data)
                db.add(zodiac)
            await db.commit()
            logger.info("Zodiacs table populated successfully.")
        except Exception as e:
            logger.error(f"Failed to populate zodiacs table: {str(e)}")
            await db.rollback()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(populate_zodiacs())
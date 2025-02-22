from app.config import settings
from app.services.ai_clients.ai_clients import get_openai_client
from openai import APIError
import logging

logger = logging.getLogger(__name__)


async def generate_ai_compatibility_description(sign1: str, sign2: str) -> str:
    """
    Генерирует текстовое описание совместимости через OpenAI.
    """
    client = get_openai_client()
    
    try:
        prompt = (
            f"Составь описание совместимости между {sign1.capitalize()} и {sign2.capitalize()}.\n"
            f"Укажи сильные и слабые стороны отношений."
        )

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    
    except (APIError, Exception) as e:
        logger.error(f"Failed to generate compatibility description: {str(e)}")
        raise


async def generate_ai_compatibility_by_bith_description(person1, person2) -> str:
    """
    Генерирует текстовое описание совместимости через OpenAI.
    """
    client = get_openai_client()
    
    try:
        
        prompt = (
            f"Создай астрологический анализ совместимости:\n"
            f"Человек 1: {person1} \n"
            f"Человек 2: {person1} \n"
        )

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        compatibility_text = response.choices[0].message.content
    
    except (APIError, Exception) as e:
        logger.error(f"Failed to generate compatibility description: {str(e)}")
        raise
from app.config import settings
from openai import AsyncOpenAI, APIError
import logging

logger = logging.getLogger(__name__)

async def generate_horoscope_text(sign: str, planetary_positions: dict, aspects: list, houses: list, interval: str='день') -> str:

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        prompt = (
            f'Составь гороскоп для знака {sign} на основе следующих данных:\n'
            f'Положения планет: {planetary_positions}\n'
            f'Аспекты: {aspects}\n'
            f'Дома: {houses}\n'
            f'Гороскоп должен быть составлен на {interval}'
        )
           
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=3000
        )
        return response.choices[0].message.content
    except (APIError, Exception) as e:
        print(f'OpenAI API error: {e}')
        return 'Не удалось сгенерировать гороскоп. Попробуйте позже.'
    
async def generate_ai_compatibility_description(sign1: str, sign2: str) -> str:
    """
    Генерирует текстовое описание совместимости через OpenAI.
    """
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

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
        return "Не удалось сгенерировать описание совместимости."
    
from app.config import settings
from app.services.ai_clients.ai_clients import get_openai_client
from openai import APIError
import openai
import asyncio
import logging

logger = logging.getLogger(__name__)

async def generate_horoscope_text(sign: str, planetary_positions: dict, aspects: list, interval: str='день') -> str:
    
    retries = 5
    delay = 2  # Начальная задержка

    for i in range(retries):
        
        client = get_openai_client()

        try:
            prompt = (
                f'Составь гороскоп для знака {sign} на основе следующих данных:\n'
                f'Положения планет и дома: {planetary_positions}\n'
                f'Аспекты: {aspects}\n'
                f'Гороскоп должен быть составлен на {interval}'
            )
            
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=2000,
                timeout=30
            )
            return response.choices[0].message.content
        
        except openai.RateLimitError:
                if i < retries - 1:
                    wait_time = delay * (2 ** i)
                    print(f"Rate limit reached. Retrying in {wait_time} sec...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
        except (APIError, Exception) as e:
            logger.error(f'OpenAI API error: {e}')
            raise
    

    
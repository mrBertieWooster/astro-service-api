from openai import AsyncOpenAI, APIError
from app.config import settings

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
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=3000
        )
        return response.choices[0].message.content
    except (APIError, Exception) as e:
        print(f'OpenAI API error: {e}')
        return 'Не удалось сгенерировать гороскоп. Попробуйте позже.'
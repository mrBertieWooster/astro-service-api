from app.config import settings
from openai import AsyncOpenAI, APIError
import openai

async def generate_natal_chart_text(planets, aspects, houses):
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    prompt = (
        f"Создай текстовое описание натальной карты с учетом:\n"
        f"- Положения планет: {planets}\n"
        f"- Аспектов: {aspects}\n"
        f"- Положения домов: {houses}\n"
    )

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=5000,
        timeout=30
    )
    return response.choices[0].message.content
from openai import OpenAI
from app.config import settings

client = OpenAI(settings.OPENAI_API_KEY)

def generate_horoscope_text(sign: str, planetary_positions: dict) -> str:
    """
    Генерирует текст гороскопа для знака зодиака на основе положений планет.
    """
    # Пример использования OpenAI API
    prompt = f"Напиши гороскоп для знака {sign} на основе следующих данных: {planetary_positions}."
    response = client.Completion.create(
        engine="gpt-4o-mini",  # Или другая модель
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
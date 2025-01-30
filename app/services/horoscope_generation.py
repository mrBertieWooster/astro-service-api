from openai import OpenAI, APIError
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_horoscope_text(sign: str, planetary_positions: dict, aspects: list, houses: list) -> str:
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        prompt = (
            f"Напиши гороскоп для знака {sign} на основе следующих данных:\n"
            f"Положения планет: {planetary_positions}\n"
            f"Аспекты: {aspects}\n"
            f"Дома: {houses}"
        )   
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000
        )
        return response.choices[0].message.content
    except APIError as e:
        print(f"Ошибка OpenAI API: {e}")
        return "Не удалось сгенерировать гороскоп. Попробуйте позже."
from app.config import settings
from openai import APIError
from app.services.ai_clients.ai_clients import get_openai_client
import json
import logging

logger = logging.getLogger(__name__)

async def generate_natal_chart_text(planets, aspects, houses, ascendant, midheaven):
    
    try:
        client = get_openai_client()

        prompt = (
            f"Создай текстовое описание натальной карты с учетом:\n"
            f"- Положения планет:\n {json.dumps(planets, indent=2, ensure_ascii=False)}\n"
            f"- Аспектов:\n {json.dumps(aspects, indent=2, ensure_ascii=False)}\n"
            f"- Положения домов:\n {json.dumps(houses, indent=2, ensure_ascii=False)}\n"
            f"- Асцендента (восходящего знака): {ascendant}\n"
            f"- Средины Неба (MC): {midheaven}\n"
            f"Проанализируй эти данные с точки зрения западной астрологии и сформируй интерпретацию."
        )

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=5000,
            timeout=30
        )

        return response.choices[0].message.content
    except APIError as ae:
        logger.error(f'Error while generating natal chart {str(ae)}')
        raise
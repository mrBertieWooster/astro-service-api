from app.services.ai_clients.ai_clients import get_openai_client
from app.config import settings
from openai import APIError
import logging

logger = logging.getLogger(__name__)

async def generate_tarot_interpretation(spread, spread_type, question=None):
    try:
        client = get_openai_client()

        prompt = (
            f"Ты — эксперт по картам Таро. Пользователь выбрал расклад '{spread_type}'.\n"
            f"Вот карты, которые выпали:\n"
            f"{spread}\n"
        )

        if question:
            prompt += f"Вопрос пользователя: {question}\n"

        prompt += "Объясни, что означает этот расклад для спрашивающего."

        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=2000,
            timeout=30
        )

        return response.choices[0].message.content
    except APIError as ae:
        logger.error(f'Error while tarot draw: {str(ae)}')
        raise


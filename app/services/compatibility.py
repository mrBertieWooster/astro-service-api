from app.services.ai_clients.openai_client.apenai_horo_generation import generate_ai_compatibility_description
import logging

logger = logging.getLogger(__name__)

async def generate_compatibility_description(sign1: str, sign2: str) -> str:
    result = await generate_ai_compatibility_description(sign1, sign2)
    logger.debug(f'compatibility result {result}')
    return result
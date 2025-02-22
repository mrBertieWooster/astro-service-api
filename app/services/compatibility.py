from app.services.ai_clients.openai_client.openai_compatibility_generation import generate_ai_compatibility_description, generate_ai_compatibility_by_bith_description
import logging

logger = logging.getLogger(__name__)

async def generate_compatibility_description(sign1: str, sign2: str) -> str:
    try:
        result = await generate_ai_compatibility_description(sign1, sign2)
        logger.debug(f'compatibility result {result}')
        return result
    except Exception as e:
        logger.error(f'Error while calculating compatibility: {str(e)}')
        raise


async def generate_compatibility_by_birth_description(person1, person2) -> str:
    try:
        result = await generate_ai_compatibility_by_bith_description(person1, person2)
        logger.debug(f'compatibility result {result}')
        return result
    except Exception as e:
        logger.error(f'Error while calculating compatibility: {str(e)}')
        raise
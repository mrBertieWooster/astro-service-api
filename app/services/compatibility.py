from app.services.ai_clients.openai_client.apenai_horo_generation import generate_ai_compatibility_description

async def generate_compatibility_description(sign1: str, sign2: str) -> str:
    await generate_ai_compatibility_description(sign1, sign2)
from app.config import settings
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

def get_openai_client():
    return openai_client

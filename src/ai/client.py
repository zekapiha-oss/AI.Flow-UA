import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_ai_client() -> OpenAI:
    """
    Ініціалізує та повертає клієнт OpenAI / DeepSeek API.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")

    if not api_key:
        raise ValueError("API-ключ не знайдено! Перевірте DEEPSEEK_API_KEY або OPENAI_API_KEY у GitHub Secrets / .env")

    return OpenAI(
        api_key=api_key,
        base_url=base_url
    )

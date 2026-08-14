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


def ask_deepseek(prompt: str, system_prompt: str = "You are a helpful assistant.", **kwargs) -> str:
    """
    Обгортка для відправки текстових запитів до DeepSeek API (використовується в analyst.py).
    """
    client = get_ai_client()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=kwargs.get("temperature", 0.3)
    )
    
    return response.choices[0].message.content.strip()

import os
from openai import OpenAI
from dotenv import load_dotenv
from src.utils.logger import logger

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
    Обгортка для відправки текстових запитів до DeepSeek API.
    """
    client = get_ai_client()

    # Захист: гарантуємо, що контент є строкою (str), а не dict чи None
    user_content = str(prompt) if not isinstance(prompt, (str, list)) else prompt
    sys_content = str(system_prompt) if system_prompt is not None else "You are a helpful assistant."

    # Якщо замість промпту передали шлях до .txt файлу, читаємо його
    if isinstance(sys_content, str) and sys_content.endswith(".txt") and os.path.exists(sys_content):
        try:
            with open(sys_content, "r", encoding="utf-8") as f:
                sys_content = f.read()
        except Exception as e:
            logger.warning(f"Не вдалося прочитати файл промпту {sys_content}: {e}")

    messages = []
    if sys_content:
        messages.append({"role": "system", "content": sys_content})
    messages.append({"role": "user", "content": user_content})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=kwargs.get("temperature", 0.3)
    )

    return response.choices[0].message.content.strip()

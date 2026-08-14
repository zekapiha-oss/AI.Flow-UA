import os
from src.ai.client import get_ai_client
from src.utils.logger import logger

def generate_post(text_content: str) -> str:
    """
    Генерує готовий пост для Telegram на основі переданого тексту/новини.
    """
    client = get_ai_client()
    
    # Завантажуємо системний промпт
    prompt_path = os.path.join("prompts", "editor.txt")
    system_prompt = "You are a professional Telegram Content Designer."
    
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text_content}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Помилка генерації поста через Editor: {e}")
        return ""

# Аліас для сумісності
generate_editor_post = generate_post

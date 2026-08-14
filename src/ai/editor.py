import os
from src.ai.client import get_ai_client
from src.utils.logger import logger

def generate_post(article_or_text) -> dict:
    """
    Генерує готовий пост для Telegram на основі переданої новини або тексту.
    Повертає словник вида {"text": "текст поста"} для повної сумісності з main.py.
    """
    client = get_ai_client()

    # 1. Формуємо чистий рядок (str), якщо передано словник (dict) або None
    if isinstance(article_or_text, dict):
        title = article_or_text.get("title", "")
        content = article_or_text.get("content") or article_or_text.get("description") or article_or_text.get("summary", "")
        url = article_or_text.get("url", "")
        user_content = f"Заголовок: {title}\n\nТекст / Опис: {content}\n\nПосилання: {url}".strip()
    elif article_or_text is None:
        user_content = ""
    else:
        user_content = str(article_or_text).strip()

    if not user_content:
        logger.warning("Передано порожній вміст для генерації поста.")
        return {"text": ""}

    # 2. Завантажуємо системний промпт
    prompt_path = os.path.join("prompts", "editor.txt")
    system_prompt = "You are a professional Telegram Content Designer."

    if os.path.exists(prompt_path):
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
        except Exception as e:
            logger.warning(f"Не вдалося прочитати prompts/editor.txt: {e}")

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3
        )

        result_text = response.choices[0].message.content.strip() if response.choices else ""
        return {"text": result_text}

    except Exception as e:
        logger.error(f"Помилка генерації поста через Editor: {e}")
        return {"text": ""}

# Аліас для сумісності з іншими викликами
generate_editor_post = generate_post

import json
from src.ai.client import get_ai_client
from src.utils.logger import logger

def generate_post(article_data: dict) -> dict:
    """
    Генерує короткий пост для Telegram на основі аналізу новини.
    """
    client = get_ai_client()
    
    try:
        with open("prompts/editor.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
    except Exception as e:
        logger.error(f"Помилка читання prompts/editor.txt: {e}")
        return {"text": "", "error": str(e)}

    title = article_data.get("title", "")
    content = article_data.get("content") or article_data.get("description") or ""
    url = article_data.get("url", "")

    user_content = (
        f"Заголовок: {title}\n"
        f"Текст новини: {content[:1200]}\n"
        f"Джерело: {url}"
    )

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            max_tokens=450,  # Ограничение длины генерации на уровне LLM API
            temperature=0.5,
            response_format={"type": "json_object"}
        )

        raw_content = response.choices[0].message.content.strip()
        data = json.loads(raw_content)

        # Вытягиваем готовый текст из JSON
        post_text = data.get("text") or data.get("post_text") or data.get("content") or ""
        
        return {
            "text": post_text.strip(),
            "raw": data
        }

    except Exception as e:
        logger.error(f"Помилка генерації поста через Editor: {e}")
        return {"text": "", "error": str(e)}

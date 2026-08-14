import os
import re
from src.ai.client import get_ai_client
from src.utils.logger import logger

# Мінімальна частка кириличних літер серед усіх літер у тексті поста,
# нижче якої вважаємо, що модель "зісковзнула" на іншу мову (не українську).
MIN_CYRILLIC_RATIO = 0.5


def _cyrillic_ratio(text: str) -> float:
    """Повертає частку кириличних літер серед усіх літер у тексті (0.0–1.0)."""
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 1.0  # немає літер (тільки емодзі/цифри/хештеги) — нема сенсу блокувати
    cyrillic = [ch for ch in letters if re.match(r'[\u0400-\u04FF]', ch)]
    return len(cyrillic) / len(letters)


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
        # Колектори кладуть посилання під ключем 'source_url', тому перевіряємо обидва варіанти.
        url = article_or_text.get("source_url") or article_or_text.get("url", "")
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

    def _call_deepseek(extra_user_note: str = "") -> str:
        content = user_content if not extra_user_note else f"{user_content}\n\n{extra_user_note}"
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip() if response.choices else ""

    try:
        result_text = _call_deepseek()

        # Перевірка мови: якщо модель відповіла переважно не українською —
        # пробуємо ще раз з явним нагадуванням, перш ніж здатися.
        if result_text and _cyrillic_ratio(result_text) < MIN_CYRILLIC_RATIO:
            logger.warning("Editor: відповідь схожа на не-українську. Повторюємо запит з нагадуванням про мову.")
            result_text = _call_deepseek(
                "ВАЖЛИВО: попередня спроба була не українською мовою. "
                "Перепиши пост ВИКЛЮЧНО українською мовою, без винятків."
            )
            if result_text and _cyrillic_ratio(result_text) < MIN_CYRILLIC_RATIO:
                logger.error("Editor: пост так і не вдалося отримати українською. Пропускаємо публікацію.")
                return {"text": ""}

        return {"text": result_text}

    except Exception as e:
        logger.error(f"Помилка генерації поста через Editor: {e}")
        return {"text": ""}

# Аліас для сумісності з іншими викликами
generate_editor_post = generate_post

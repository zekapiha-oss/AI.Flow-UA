import os
import re
import requests
from src.utils.logger import logger


def _strip_html_tags(text: str) -> str:
    """Прибирає HTML-теги форматування для чистого текстового фолбеку."""
    return re.sub(r"</?(b|i|u|a)[^>]*>", "", text)

def send_telegram_message(text: str) -> bool:
    """
    Відправляє сформований пост у Telegram-канал через Telegram Bot API.
    Повертає True у разі успіху, інакше False.
    """
    if not text:
        logger.error("Текст для публікації порожній.")
        return False

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID")

    if not bot_token or not chat_id:
        logger.error("Відсутній TELEGRAM_BOT_TOKEN або TELEGRAM_CHAT_ID у GitHub Secrets / .env")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return True

        # Спроба фолбеку: якщо Telegram повернув помилку через синтаксис HTML
        # (наприклад, модель залишила незакритий тег або зайвий символ < чи &),
        # надсилаємо як простий текст без форматування.
        logger.warning(f"Не вдалося надіслати з HTML (код {response.status_code}). Пробуємо чистий текст...")
        payload.pop("parse_mode", None)
        payload["text"] = _strip_html_tags(text)

        fallback_response = requests.post(url, json=payload, timeout=10)
        if fallback_response.status_code == 200:
            return True

        logger.error(f"Помилка Telegram API: {fallback_response.text}")
        return False

    except Exception as e:
        logger.error(f"Виняток при відправці повідомлення в Telegram: {e}")
        return False


# Аліас для сумісності, якщо десь викливається під іншою назвою
def publish_message(text: str) -> bool:
    return send_telegram_message(text)

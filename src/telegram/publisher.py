import os
import requests
from src.utils.logger import log_info, log_error

def publish_message(text: str) -> dict:
    """
    Відправляє повідомлення у Telegram-канал.
    Використовує метод sendMessage офіційного API.
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHANNEL_ID')
    disable_preview = os.getenv('DISABLE_LINK_PREVIEW', 'true').lower() == 'true'

    if not token or not chat_id:
        log_error("Відсутні TELEGRAM_BOT_TOKEN або TELEGRAM_CHANNEL_ID")
        return {"success": False, "error": "Missing credentials"}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Параметри згідно з ТЗ
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview
    }

    try:
        # Встановлено timeout згідно з Розділом 49 ТЗ
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            msg_id = data['result']['message_id']
            log_info(f"Telegram: published (Message ID: {msg_id})")
            return {"success": True, "message_id": msg_id}
        else:
            log_error(f"Telegram API Error: {data.get('description')}")
            return {"success": False, "error": data.get('description')}
            
    except requests.exceptions.RequestException as e:
        log_error(f"Помилка мережі при відправці в Telegram: {str(e)}")
        return {"success": False, "error": str(e)}

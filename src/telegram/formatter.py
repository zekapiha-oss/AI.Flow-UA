from src.utils.logger import logger

def format_post(text: str, article_url: str = "") -> str:
    """
    Форматує текст поста для Telegram та додає посилання на джерело.
    """
    if not text:
        return ""

    formatted_text = text.strip()

    # Додаємо посилання на джерело у форматі Telegram HTML, якщо воно є та ще не присутнє в тексті
    if article_url and article_url not in formatted_text:
        formatted_text += f'\n\n🔗 <a href="{article_url}">Читати джерело</a>'

    return formatted_text

# Альтернативна назва для сумісності з іншими модулями
def format_telegram_message(text: str, url: str = "") -> str:
    return format_post(text, article_url=url)

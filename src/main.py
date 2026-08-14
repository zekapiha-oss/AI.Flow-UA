import sys
from src.collectors.newsdata import fetch_newsdata
from src.collectors.hackernews import fetch_hackernews
from src.ai.editor import generate_post
from src.telegram.formatter import format_post
from src.telegram.publisher import send_telegram_message
from src.deduplication.detector import is_duplicate, save_processed_news
from src.utils.validators import validate_character_limit
from src.utils.logger import logger


def run_pipeline():
    logger.info("--- Запуск AI News Pipeline ---")

    # 1. Сбор новостей
    newsdata_items = fetch_newsdata() or []
    hn_items = fetch_hackernews() or []
    all_articles = newsdata_items + hn_items

    logger.info(f"Зібрано {len(all_articles)} новин для перевірки.")

    published_count = 0

    for article in all_articles:
        title = article.get("title", "Без заголовка")
        # Колектори (newsdata.py, hackernews.py) кладуть посилання під ключем
        # 'source_url', а не 'url'. Беремо обидва варіанти для сумісності,
        # інакше url завжди порожній і дедуплікація/лінк у пості не працюють.
        url = article.get("source_url") or article.get("url", "")

        logger.info(f"Обробка новини: {title}")

        # 2. Дедупликация
        if is_duplicate(url):
            logger.info("Новина вже оброблена раніше. Пропускаємо.")
            continue

        # 3. Генерация текста поста (Editor) напрямую
        logger.info("Генерація посту через DeepSeek Editor...")
        editor_result = generate_post(article)
        if isinstance(editor_result, dict):
            post_text = editor_result.get("text", "")
        elif isinstance(editor_result, str):
            post_text = editor_result
        else:
            post_text = ""

        if not post_text:
            logger.error("Редактор не зміг згенерувати текст поста.")
            continue

        logger.info("Editor успішно згенерував текст.")

        # 4. Форматирование текста для Telegram
        formatted_post = format_post(post_text, article_url=url) if callable(format_post) else post_text

        # 5. Проверка лимита символов (<= 777 символов)
        if not validate_character_limit(formatted_post, limit=999):
            continue

        # 6. Публикация в Telegram
        published = send_telegram_message(formatted_post)
        if published:
            logger.info(f"Успішно опубліковано в Telegram: {title}")
            save_processed_news(url, title)
            published_count += 1
            # Публикуем 1 свежую новость за один запуск пайплайна
            break
        else:
            logger.error("Помилка публікації в Telegram.")

    logger.info(f"--- Пайплайн завершив роботу. Опубліковано постів: {published_count} ---")


if __name__ == "__main__":
    run_pipeline()

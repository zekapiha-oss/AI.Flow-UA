import os
import time
from dotenv import load_dotenv

from src.config import DRY_RUN, MIN_SCORE, MAX_POSTS_PER_RUN
from src.database.storage import init_db, insert_news
from src.collectors.newsdata import fetch_newsdata
from src.collectors.hackernews import fetch_hackernews
from src.deduplication.detector import is_duplicate
from src.ai.analyst import analyze_news
from src.ai.editor import generate_post
from src.ai.quality import check_quality
from src.telegram.formatter import build_message, count_characters
from src.telegram.publisher import publish_message
from src.utils.validators import validate_character_limit
from src.utils.logger import log_info, log_error

def main():
    load_dotenv()
    init_db()
    
    log_info('--- Запуск AI News Pipeline ---')
    if DRY_RUN:
        log_info('Режим DRY_RUN увімкнено (без реальної публікації)')

    # 1. Збір новин (за ТЗ об'єднуємо джерела)
    articles = []
    articles.extend(fetch_newsdata())
    articles.extend(fetch_hackernews())
    
    log_info(f'Зібрано {len(articles)} новин для перевірки.')

    published_count = 0

    for article in articles:
        # 2. Дедуплікація
        if is_duplicate(article['source_url'], article['title']):
            continue
            
        # Зберігаємо в базу зі статусом NEW
        if not insert_news(article):
            continue

        log_info(f"Аналізуємо: {article['title']}")
        
        # 3. Аналіз AI Analyst
        text_to_analyze = f"Title: {article['title']}\nContent: {article['content']}"
        analysis = analyze_news(text_to_analyze)
        
        if not analysis:
            continue
            
        score = analysis.get('TOTAL_SCORE', 0)
        if score < MIN_SCORE:
            log_info(f'Новину відхилено (Score: {score} < {MIN_SCORE})')
            continue
            
        log_info(f'Новину прийнято (Score: {score}). Передаємо Редактору...')
        
        # 4. Редактура AI Editor
        editor_payload = {
            'title': article['title'],
            'facts': text_to_analyze,
            'score': score,
            'context': analysis,
            'ukraine_context': analysis.get('UKRAINE', 0)
        }
        post_data = generate_post(editor_payload)
        
        if not post_data:
            continue
            
        post_data['source_url'] = article['source_url']
        
        # 5. Контроль якості
        if not check_quality(post_data):
            log_error('Пост не пройшов контроль якості AI.')
            continue
            
        # 6. Форматування та перевірка 777 символів
        final_message = build_message(post_data)
        char_count = count_characters(final_message)
        
        if not validate_character_limit(final_message):
            log_error(f'Перевищено ліміт символів: {char_count} > 777. Пропускаємо.')
            continue
            
        # 7. Публікація в Telegram
        if DRY_RUN:
            log_info(f'[DRY RUN] Готовий пост ({char_count} симв.):\n\n{final_message}\n')
            published_count += 1
        else:
            result = publish_message(final_message)
            if result.get('success'):
                published_count += 1
                log_info('Успішно опубліковано!')
                time.sleep(3) # Захист від Rate Limits Telegram
            else:
                log_error('Помилка публікації.')
                
        # Зупиняємось, якщо досягли ліміту постів за один запуск
        if published_count >= MAX_POSTS_PER_RUN:
            log_info(f'Досягнуто ліміт публікацій на цей запуск ({MAX_POSTS_PER_RUN}).')
            break

    log_info('--- Пайплайн завершив роботу ---')

if __name__ == '__main__':
    main()

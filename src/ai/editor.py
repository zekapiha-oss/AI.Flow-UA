import json
from src.ai.client import ask_deepseek
from src.utils.logger import log_info

def generate_post(news_data: dict) -> dict:
    """
    Отримує факти, score, контекст та створює оригінальний пост.
    Повертає структурований JSON (publish, title, lead, facts, impact, ukraine_impact, diary, hashtags).
    Згідно з ТЗ, AI не генерує HTML (це робить Python).
    """
    log_info('Генерація посту через DeepSeek Editor...')
    
    # Перетворюємо вхідні дані на JSON-рядок для передачі в AI
    prompt = json.dumps(news_data, ensure_ascii=False)
    result = ask_deepseek(prompt, 'editor.txt')
    
    if result:
        log_info('Editor успішно згенерував текст (JSON).')
        return result
    return None

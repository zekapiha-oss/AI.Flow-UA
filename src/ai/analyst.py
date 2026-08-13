from src.ai.client import ask_deepseek
from src.utils.logger import log_info

def analyze_news(article_text: str) -> dict:
    """
    Аналізує подію, визначає факти та наслідки.
    Повертає оцінки (0-10): NOVELTY, IMPORTANCE, PRACTICAL, AI_RELEVANCE, UKRAINE, VIRALITY
    """
    log_info('Аналіз новини через DeepSeek Analyst...')
    result = ask_deepseek(article_text, 'analyst.txt')
    
    if result:
        # Підрахунок TOTAL_SCORE згідно з ТЗ
        scores = [
            result.get('NOVELTY', 0), 
            result.get('IMPORTANCE', 0),
            result.get('PRACTICAL', 0), 
            result.get('AI_RELEVANCE', 0),
            result.get('UKRAINE', 0), 
            result.get('VIRALITY', 0)
        ]
        result['TOTAL_SCORE'] = sum(scores)
        log_info(f"Оцінка Analyst: {result['TOTAL_SCORE']} балів")
        return result
    return None

import os
import requests
from src.utils.logger import log_error, log_info

def fetch_newsdata() -> list:
    """Збирає новини через NewsData.io API за визначеними ключовими словами."""
    api_key = os.getenv('NEWSDATA_API_KEY')
    if not api_key:
        log_error("Відсутній NEWSDATA_API_KEY")
        return []

    # Запити згідно з ТЗ (укорочено, щоб влізти в ліміт довжини q на безкоштовному плані NewsData.io)
    query = "AI OR \"Artificial Intelligence\" OR \"AI Agents\" OR \"Generative AI\" OR \"AI Startup\""
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": api_key,
        "q": query,
        "language": "en",
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for item in data.get('results', []):
            articles.append({
                'source': 'NewsData',
                'source_id': item.get('article_id'),
                'source_url': item.get('link'),
                'title': item.get('title'),
                'description': item.get('description', ''),
                'content': item.get('content', '') or item.get('description', '')
            })
        log_info(f"NewsData: знайдено {len(articles)} статей")
        return articles
    except Exception as e:
        log_error(f"Помилка NewsData API: {e}")
        return []

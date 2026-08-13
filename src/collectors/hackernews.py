import requests
from src.utils.logger import log_error, log_info

def fetch_hackernews() -> list:
    """Збирає новини через офіційний API Hacker News (API key не потрібен)."""
    try:
        # Отримуємо останні історії
        url = "https://hacker-news.firebaseio.com/v0/newstories.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        story_ids = response.json()[:15] # Беремо перші 15 для MVP
        
        articles = []
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_res = requests.get(story_url, timeout=10)
            if story_res.status_code == 200:
                story = story_res.json()
                if story and story.get('url'):
                    articles.append({
                        'source': 'HackerNews',
                        'source_id': str(story.get('id')),
                        'source_url': story.get('url'),
                        'title': story.get('title'),
                        'description': '',
                        'content': ''
                    })
        log_info(f"Hacker News: знайдено {len(articles)} статей")
        return articles
    except Exception as e:
        log_error(f"Помилка Hacker News API: {e}")
        return []

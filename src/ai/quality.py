from src.utils.validators import validate_hashtags

def check_quality(post_data: dict) -> bool:
    """
    Проводить контроль якості JSON-даних, згенерованих Editor-ом.
    Якщо хоча б одна обов'язкова перевірка не пройдена — повертає False.
    """
    required_keys = ['title', 'lead', 'diary', 'hashtags', 'source_url']
    
    # Перевірка наявності всіх необхідних блоків
    for key in required_keys:
        if not post_data.get(key):
            return False
            
    # Перевірка хештегів
    if not validate_hashtags(post_data.get('hashtags', [])):
        return False
        
    # Базова перевірка на наявність емодзі в заголовку (суворий критерій ТЗ)
    import emoji
    if not emoji.emoji_count(post_data['title']) > 0:
        return False
        
    return True

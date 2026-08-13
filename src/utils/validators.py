import re

def validate_character_limit(message: str, limit: int = 777) -> bool:
    """Перевіряє, чи не перевищує фінальне повідомлення ліміт (за замовчуванням 777)."""
    return len(message) <= limit

def validate_hashtags(hashtags: list) -> bool:
    """Перевірка: тільки англійська мова та від 3 до 6 хештегів."""
    if not isinstance(hashtags, list):
        return False
    if not (3 <= len(hashtags) <= 6):
        return False
    
    # Перевірка, що хештеги складаються лише з англійських літер та цифр
    english_pattern = re.compile(r'^#[A-Za-z0-9_]+$')
    for tag in hashtags:
        if not english_pattern.match(tag):
            return False
    return True

import hashlib
from src.database.storage import get_connection

def generate_hash(text: str) -> str:
    if not text:
        return ""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def is_duplicate(url: str, title: str) -> bool:
    """
    Перевіряє, чи не публікувалася ця новина раніше.
    1. Перевірка URL (абсолютний збіг).
    2. Перевірка заголовка (абсолютний збіг).
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Перевірка за URL
        cursor.execute("SELECT id FROM news WHERE source_url = ?", (url,))
        if cursor.fetchone():
            return True
            
        # Перевірка за заголовком
        cursor.execute("SELECT id FROM news WHERE title = ?", (title,))
        if cursor.fetchone():
            return True
            
    return False

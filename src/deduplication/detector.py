import sqlite3
import hashlib
import os
from src.utils.logger import logger

DB_PATH = os.path.join("data", "database.sqlite")

def _init_db():
    """Ініціалізація таблиці дедуплікації в базі даних SQLite."""
    os.makedirs("data", exist_ok=True)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url_hash TEXT UNIQUE,
                    url TEXT,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except Exception as e:
        logger.error(f"Помилка ініціалізації БД дедуплікації: {e}")

def _hash_url(url: str) -> str:
    """Генерує MD5-хеш для перевірки унікальності URL."""
    return hashlib.md5(url.strip().lower().encode('utf-8')).hexdigest()

def is_duplicate(url: str) -> bool:
    """
    Перевіряє, чи була новина вже оброблена та опублікована раніше.
    """
    if not url:
        return False

    _init_db()
    url_hash = _hash_url(url)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM processed_news WHERE url_hash = ?", (url_hash,))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        logger.error(f"Помилка перевірки дедуплікації: {e}")
        return False

def save_processed_news(url: str, title: str = "") -> bool:
    """
    Зберігає оброблену новину в базу даних, щоб уникнути повторних публікацій.
    """
    if not url:
        return False

    _init_db()
    url_hash = _hash_url(url)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO processed_news (url_hash, url, title) VALUES (?, ?, ?)",
                (url_hash, url, title)
            )
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Помилка збереження новини в БД дедуплікації: {e}")
        return False

# Аліаси для сумісності з іншими варіантами викликів
def mark_as_processed(url: str, title: str = "") -> bool:
    return save_processed_news(url, title)

def add_processed_news(url: str, title: str = "") -> bool:
    return save_processed_news(url, title)

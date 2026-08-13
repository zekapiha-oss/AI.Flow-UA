import os
import sqlite3
from contextlib import contextmanager
from src.config import DB_PATH


def _ensure_db_dir():
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)


@contextmanager
def get_connection():
    """Повертає з'єднання з базою даних як контекстний менеджер."""
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Створює таблицю, якщо її ще не існує."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT UNIQUE,
                title TEXT,
                summary TEXT,
                score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def insert_news(article: dict) -> bool:
    """Додає нову статтю в базу. Повертає False, якщо URL вже існує."""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO news (source_url, title, summary, score)
                VALUES (?, ?, ?, ?)
            """, (
                article.get('source_url'),
                article.get('title'),
                article.get('description', ''),
                article.get('score', 0),
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

from src.utils.logger import logger

MAX_CHARACTER_LIMIT = 777

def validate_character_limit(text: str, limit: int = MAX_CHARACTER_LIMIT) -> bool:
    """
    Перевіряє, чи не перевищує довжина ГОТОВОГО тексту поста встановлений ліміт символів.
    """
    if not text:
        logger.warning("Валідація не пройшла: текст порожній.")
        return False

    length = len(text)
    if length > limit:
        logger.error(f"Перевищено ліміт символів: {length} > {limit}. Пропускаємо.")
        return False

    return True

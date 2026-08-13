import emoji
from src.utils.validators import validate_hashtags
from src.utils.logger import log_error

def check_quality(post_data: dict) -> bool:
    """
    Проводить контроль якості JSON-даних, згенерованих Editor-ом.
    Якщо хоча б одна обов'язкова перевірка не пройдена — повертає False
    і пише в лог ТОЧНУ причину відмови (для діагностики).
    """
    required_keys = ['title', 'lead', 'diary', 'hashtags', 'source_url']

    # Перевірка наявності всіх необхідних блоків
    for key in required_keys:
        if not post_data.get(key):
            log_error(f"Quality: відсутнє або порожнє поле '{key}'. Отримано: {post_data.get(key)!r}")
            return False

    # Перевірка хештегів
    hashtags = post_data.get('hashtags', [])
    if not validate_hashtags(hashtags):
        log_error(f"Quality: хештеги не пройшли валідацію. Отримано: {hashtags!r}")
        return False

    # Базова перевірка на наявність емодзі в заголовку (суворий критерій ТЗ)
    title = post_data['title']
    if emoji.emoji_count(title) == 0:
        log_error(f"Quality: у заголовку немає emoji. Заголовок: {title!r}")
        return False

    return True

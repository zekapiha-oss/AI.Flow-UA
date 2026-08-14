import logging
import sys

# Налаштування формату та виводу логів
logger = logging.getLogger("AI.Flow-UA")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_logger():
    """Повертає екземпляр логера."""
    return logger

# Функції-обгортки для зворотної сумісності з колекторами новин
def log_info(message: str):
    """Логування інформаційного повідомлення."""
    logger.info(message)

def log_error(message: str):
    """Логування помилки."""
    logger.error(message)

def log_warning(message: str):
    """Логування попередження."""
    logger.warning(message)

def log_debug(message: str):
    """Логування налагоджувальної інформації."""
    logger.debug(message)

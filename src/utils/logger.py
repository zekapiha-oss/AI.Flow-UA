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
    """Повертає вже налаштований екземпляр логера."""
    return logger

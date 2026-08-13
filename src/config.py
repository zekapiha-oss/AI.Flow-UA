import os

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
MAX_MESSAGE_LENGTH = 777
MAX_POSTS_PER_RUN = int(os.getenv("MAX_POSTS_PER_RUN", 1))
MAX_POSTS_PER_HOUR = int(os.getenv("MAX_POSTS_PER_HOUR", 3))
MAX_POSTS_PER_DAY = int(os.getenv("MAX_POSTS_PER_DAY", 15))
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", 15))
MIN_SCORE = int(os.getenv("MIN_SCORE", 65))
LANGUAGE = "uk"
TELEGRAM_PARSE_MODE = "HTML"
DISABLE_LINK_PREVIEW = os.getenv("DISABLE_LINK_PREVIEW", "true").lower() == "true"

DB_PATH = os.getenv("DB_PATH", "data/database.sqlite")

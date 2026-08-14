import os
import re
from src.ai.client import ask_deepseek
from src.utils.logger import logger

def analyze_news(article: dict) -> int:
    """
    Аналізує важливість та релевантність новини за допомогою DeepSeek Analyst.
    Повертає числову оцінку (score) від 0 до 500.
    """
    if not isinstance(article, dict):
        logger.error("Некоректний формат даних новини для аналізу (очікувався dict).")
        return 0

    title = article.get("title", "")
    content = article.get("content") or article.get("description") or ""

    # Формуємо чіткий текстовий промпт для моделі (перетворюємо об'єкт у рядок)
    user_prompt = (
        f"Заголовок: {title}\n"
        f"Текст / Опис: {content[:1500]}\n\n"
        f"Оціни актуальність та цінність цієї новини для AI-спільноти за шкалою від 0 до 500. "
        f"Поверни ТІЛЬКИ число оцінки (наприклад, 350)."
    )

    # Читаємо системний промпт із файлу prompts/analyst.txt
    system_prompt = "You are an AI news analyst. Rate news importance from 0 to 500. Return only the number score."
    prompt_path = os.path.join("prompts", "analyst.txt")
    
    if os.path.exists(prompt_path):
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                system_prompt = f.read()
        except Exception as e:
            logger.warning(f"Не вдалося прочитати prompts/analyst.txt: {e}. Використовуємо стандартний промпт.")

    try:
        response_text = ask_deepseek(user_prompt, system_prompt=system_prompt)

        # Витягуємо перше число з відповіді моделі
        numbers = re.findall(r'\d+', response_text)
        if numbers:
            score = int(numbers[0])
            return score
        else:
            logger.warning(f"Analyst повернув текст без чисел: '{response_text}'. Надаємо оцінку 200.")
            return 200

    except Exception as e:
        logger.error(f"Помилка при аналізі новини в Analyst: {e}")
        return 0

import os
import json
from openai import OpenAI
from src.utils.logger import log_error, log_info

def ask_deepseek(prompt: str, system_file: str) -> dict:
    """Відправляє запит до DeepSeek API та гарантовано повертає JSON."""
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        log_error('DEEPSEEK_API_KEY не знайдено!')
        return None
        
    try:
        # Читаємо промпт з відповідного файлу згідно зі структурою ТЗ
        with open(f'prompts/{system_file}', 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except Exception as e:
        log_error(f'Помилка читання промпту {system_file}: {e}')
        return None

    # Використовуємо бібліотеку OpenAI, оскільки DeepSeek API з нею сумісний
    client = OpenAI(api_key=api_key, base_url='https://api.deepseek.com/v1')
    
    try:
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            response_format={'type': 'json_object'},
            timeout=60
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        log_error(f'Помилка DeepSeek API: {e}')
        return None

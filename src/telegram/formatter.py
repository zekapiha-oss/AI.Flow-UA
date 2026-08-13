def build_title(title: str) -> str:
    return f"<b>{title}</b>\n\n"

def build_body(lead: str) -> str:
    return f"{lead}\n\n"

def build_facts(facts: list) -> str:
    if not facts:
        return ""
    facts_str = '\n'.join([f"• <b>{f}</b>" for f in facts])
    return f"{facts_str}\n\n"

def build_impact(impact: str) -> str:
    return f"💡 {impact}\n\n" if impact else ""

def build_ukraine(ukraine_context: str) -> str:
    return f"🇺🇦 {ukraine_context}\n\n" if ukraine_context else ""

def build_diary(diary_text: str) -> str:
    return f"💭 Мій щоденник\n<blockquote>{diary_text}</blockquote>\n\n" if diary_text else ""

def build_source(url: str) -> str:
    return f"🔗 <a href='{url}'>Джерело</a>\n\n" if url else ""

def build_hashtags(tags: list) -> str:
    return " ".join(tags) if tags else ""

def build_message(data: dict) -> str:
    """Збирає фінальне повідомлення з усіх блоків, формуючи HTML."""
    message = ""
    message += build_title(data.get('title', ''))
    message += build_body(data.get('lead', ''))
    message += build_facts(data.get('facts', []))
    message += build_impact(data.get('impact', ''))
    message += build_ukraine(data.get('ukraine_impact', ''))
    message += build_diary(data.get('diary', ''))
    message += build_source(data.get('source_url', ''))
    message += build_hashtags(data.get('hashtags', []))
    return message.strip()

def count_characters(message: str) -> int:
    return len(message)

# AI News Telegram Bot

Автоматичний пайплайн: збирає новини (NewsData.io, Hacker News), аналізує та
редагує їх через DeepSeek API, перевіряє якість і публікує в Telegram-канал.
Розрахований на запуск за розкладом у GitHub Actions.

## Локальний запуск

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # заповніть власними ключами
python -m src.main
```

Запускати саме як модуль (`python -m src.main`), а не `python src/main.py` —
інакше зламаються абсолютні імпорти пакета `src`.

## Змінні середовища

| Змінна | Призначення |
|---|---|
| `TELEGRAM_BOT_TOKEN` | токен Telegram-бота |
| `TELEGRAM_CHANNEL_ID` | ID каналу для публікації |
| `DEEPSEEK_API_KEY` | ключ DeepSeek API |
| `NEWSDATA_API_KEY` | ключ NewsData.io |
| `PRODUCTHUNT_CLIENT_ID` / `PRODUCTHUNT_CLIENT_SECRET` | для колектора Product Hunt (наразі заглушка) |
| `DRY_RUN` | `true` — не публікувати, лише виводити в лог |
| `DB_PATH` | шлях до sqlite-бази дедуплікації (за замовчуванням `data/database.sqlite`) |

## GitHub Actions

Workflow `.github/workflows/news_bot.yml` запускається за розкладом (кожні
15 хв) і вручну (`workflow_dispatch`). Секрети (`Settings -> Secrets and
variables -> Actions -> Secrets`):

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHANNEL_ID`
- `DEEPSEEK_API_KEY`
- `NEWSDATA_API_KEY`
- `PRODUCTHUNT_CLIENT_ID`
- `PRODUCTHUNT_CLIENT_SECRET`

Опційна repo-змінна (`Variables`, не Secrets): `DRY_RUN=true`, якщо потрібно
тимчасово вимкнути реальні публікації.

База даних дедуплікації (`data/database.sqlite`) комітиться назад у репозиторій
після кожного запуску, щоб бот пам'ятав, що вже публікував, між запусками
ефемерних runner'ів.

ВАЖЛИВО: ніколи не комітьте `.env` — він вже у `.gitignore`. Якщо ключі з
`.env` колись потрапляли в git-історію чи були кимось побачені, обов'язково
перевипустіть (ротуйте) їх у відповідних сервісах.

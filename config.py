import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"  # можно заменить на "gpt-4o-mini"

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

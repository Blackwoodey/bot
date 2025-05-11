import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "ft:gpt-4o-mini-2024-07-18:ksenia::BLs17yBi"

# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")

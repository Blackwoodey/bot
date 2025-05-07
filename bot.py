from dotenv import load_dotenv
load_dotenv()
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user_input

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_input.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

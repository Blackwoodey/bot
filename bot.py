from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import BOT_TOKEN
from handlers import user_input

router = Router()

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Изменить промт")]
    ],
    resize_keyboard=True
)

# Команда для открытия меню
@router.message(F.text == "/menu")
async def show_menu(message: Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)

# Обработка кнопки
@router.message(F.text == "📝 Изменить промт")
async def prompt_change_request(message: Message):
    if str(message.from_user.id) not in ["791851827", "689955387"]:
        return await message.answer("У вас нет доступа к изменению промта.")
    
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            current_prompt = f.read()
    except Exception:
        current_prompt = "[Промт ещё не задан]"

    await message.answer(
        f"📄 Текущий промт:\n\n{current_prompt}\n\n✍️ Введите новый промт:",
        reply_markup=ReplyKeyboardRemove()
    )

    with open(".prompt_state", "w") as f:
        f.write(str(message.from_user.id))

# Обработка ввода нового промта
@router.message()
async def catch_prompt(message: Message):
    if not os.path.exists(".prompt_state"):
        return

    with open(".prompt_state", "r") as f:
        waiting_id = f.read().strip()

    if str(message.from_user.id) != waiting_id:
        return

    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(message.text)

    os.remove(".prompt_state")
    await message.answer("Промт успешно обновлён ✅", reply_markup=main_keyboard)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_input.router)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

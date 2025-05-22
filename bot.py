from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from handlers import user_input
from services.gpt_core import get_temperature, set_temperature

# ✅ Импортируем роутер из нового модуля
from prompt_editor import router as prompt_editor_router

router = Router()

ADMINS = {"791851827", "689955387"}

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📝 Изменить промт")],
        [KeyboardButton(text="🌡️ Изменить температуру")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "/menu")
async def show_menu(message: Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)

# Кнопка "Изменить температуру"
@router.message(F.text == "🌡️ Изменить температуру")
async def temperature_change_request(message: Message):
    if str(message.from_user.id) not in ADMINS:
        return await message.answer("⛔ У вас нет доступа к изменению температуры.")

    try:
        current_temp = get_temperature()
    except:
        current_temp = "1.0 (по умолчанию)"

    await message.answer(
        f"🌡️ Текущая температура: {current_temp}\n\n✍️ Введите новое значение от 0.0 до 2.0:",
        reply_markup=None
    )

    with open(".temperature_state", "w") as f:
        f.write(str(message.from_user.id))

# Обработка ввода новой температуры
@router.message()
async def catch_temperature(message: Message):
    user_id = str(message.from_user.id)

    # Температура
    if os.path.exists(".temperature_state"):
        with open(".temperature_state", "r") as f:
            waiting_id = f.read().strip()

        if user_id == waiting_id:
            try:
                new_temp = float(message.text.strip())
                if not (0 <= new_temp <= 2):
                    raise ValueError
                set_temperature(new_temp)
                await message.answer("✅ Температура обновлена", reply_markup=main_keyboard)
            except:
                await message.answer("❌ Некорректное значение. Введи число от 0.0 до 2.0 (например: 0.7)")
            os.remove(".temperature_state")
            return

# Запуск бота
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_input.router)
    dp.include_router(prompt_editor_router)  # подключаем редактор промтов
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

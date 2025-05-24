from dotenv import load_dotenv
load_dotenv()

import asyncio
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from config import BOT_TOKEN
from handlers.stage3_direction import suggest_path_from_arch
from prompt_editor import router as prompt_editor_router

router = Router()
ADMINS = {"791851827", "689955387"}

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📈 Изменить промт")],
        [KeyboardButton(text="🌡️ Изменить температуру")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие:"
)

# Контексты пользователей и таймеры
user_context = {}
timeout_tasks = {}

@router.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_keyboard)

# ⏳ Обработка этапа 2 (установка архетипа)
@router.message(F.text.startswith("архетип: "))
async def handle_arch_setup(message: Message):
    arch = message.text.replace("архетип: ", "").strip()
    user_id = message.from_user.id
    user_context[user_id] = {"arch": arch, "stage": 3}

    # Запускаем таймер — через 180 секунд проверим, ответил ли пользователь
    if user_id in timeout_tasks:
        timeout_tasks[user_id].cancel()

    timeout_tasks[user_id] = asyncio.create_task(send_fallback_if_no_reply(user_id, arch))
    await message.answer("🌀 Архетип получен. Жду твоего отклика...")

# 🧠 Обработка ответа пользователя (после архетипа)
@router.message()
async def handle_user_reply(message: Message):
    user_id = message.from_user.id
    ctx = user_context.get(user_id)

    if ctx and ctx.get("stage") == 3:
        arch = ctx["arch"]
        user_input = message.text

        # Останавливаем таймер
        if user_id in timeout_tasks:
            timeout_tasks[user_id].cancel()
            del timeout_tasks[user_id]

        reply = await suggest_path_from_arch(arch_name=arch, user_answer=user_input)
        await message.answer(reply)
        user_context[user_id]["stage"] = 4  # переходим к следующему этапу

async def send_fallback_if_no_reply(user_id: int, arch: str):
    await asyncio.sleep(180)
    reply = await suggest_path_from_arch(arch_name=arch, user_answer=None)
    await bot.send_message(chat_id=user_id, text=reply)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.include_router(prompt_editor_router)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import os

# ✅ Список Telegram ID админов
ADMINS = {689955387, 791851827}

router = Router()

# ✅ Пути к файлам промтов с понятными названиями
PROMPT_PATHS = {
    "🌐 Общий (начальный)": "prompt.txt",
    "🌀 Этап 2 — Вопрос": "prompts/stage2.txt",
    "🧭 Этап 3 — Архетип боли": "prompts/stage3.txt",
    "🔁 Этап 3b — Направление": "prompts/stage3b.txt",
    "💬 Этап 4 — Вовлечение и предложение": "prompts/stage4.txt"
}

class PromptEdit(StatesGroup):
    choosing = State()
    editing = State()

@router.message(Command("edit_prompt"))
async def edit_prompt_command(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("⛔ Только админ может редактировать промты.")

    kb = InlineKeyboardBuilder()
    for title in PROMPT_PATHS:
        kb.button(text=title, callback_data=title)
    await msg.answer("Выбери файл промта для редактирования:", reply_markup=kb.as_markup())
    await state.set_state(PromptEdit.choosing)

# 🔁 Обработка кнопки из меню "📝 Изменить промт"
@router.message(F.text.contains("Изменить промт"))
async def prompt_menu_button(msg: Message, state: FSMContext):
    await edit_prompt_command(msg, state)

@router.callback_query(PromptEdit.choosing)
async def show_current_prompt(callback: CallbackQuery, state: FSMContext):
    file_key = callback.data
    file_path = PROMPT_PATHS.get(file_key)
    if not file_path:
        return await callback.message.answer("❌ Не удалось найти путь к выбранному промту.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            current_text = f.read()
    except Exception as e:
        return await callback.message.answer(f"Ошибка чтения файла: {e}")

    await state.update_data(file_path=file_path)
    await callback.message.answer(
        f"📄 Сейчас установлен промт:\n\n<code>{current_text[:3000]}</code>\n\n✏️ Отправь новый текст для замены.",
        parse_mode="HTML"
    )
    await state.set_state(PromptEdit.editing)
    await callback.answer()

@router.message(PromptEdit.editing, F.text)
async def save_new_prompt(msg: Message, state: FSMContext):
    data = await state.get_data()
    file_path = data.get("file_path")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(msg.text)
        await msg.answer("✅ Промт успешно обновлён.")
    except Exception as e:
        await msg.answer(f"❌ Ошибка при сохранении: {e}")
    await state.clear()

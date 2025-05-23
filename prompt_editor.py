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

# ✅ Краткие ключи → (название кнопки, путь к файлу)
PROMPT_PATHS = {
    "core": ("Основной промт (gpt)", "prompt.txt"),
    "stage2": ("Этап 2: вопрос", "prompts/stage2.txt"),
    "stage3": ("Этап 3: распознавание", "prompts/stage3.txt"),
    "stage3b": ("Этап 3б: предложение пути", "prompts/stage3b.txt"),
    "stage4": ("Этап 4: вовлечение", "prompts/stage4.txt")
}

# ✅ Состояния FSM
class PromptEdit(StatesGroup):
    choosing = State()
    editing = State()

# ✅ Команда /edit_prompt
@router.message(Command("edit_prompt"))
async def edit_prompt_command(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("⛔ Только админ может редактировать промты.")

    kb = InlineKeyboardBuilder()
    for key, (label, _) in PROMPT_PATHS.items():
        kb.button(text=label, callback_data=key)

    await msg.answer("Выбери файл промта для редактирования:", reply_markup=kb.as_markup())
    await state.set_state(PromptEdit.choosing)

# ✅ Обработка нажатия на кнопку выбора файла
@router.callback_query(PromptEdit.choosing)
async def show_current_prompt(callback: CallbackQuery, state: FSMContext):
    file_key = callback.data
    if file_key not in PROMPT_PATHS:
        return await callback.message.answer("❌ Неизвестный файл.")

    _, file_path = PROMPT_PATHS[file_key]

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

# ✅ Сохранение нового текста промта
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

# ✅ Обработка кнопки из меню "📝 Изменить промт"
@router.message(F.text == "📝 Изменить промт")
async def prompt_menu_button(msg: Message, state: FSMContext):
    await edit_prompt_command(msg, state)

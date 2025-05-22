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

# ✅ Пути к файлам промтов
PROMPT_PATHS = {
    "prompt.txt": "prompt.txt",
    "stage2.txt": "prompts/stage2.txt",
    "stage3.txt": "prompts/stage3.txt",
    "stage3b.txt": "prompts/stage3b.txt",
    "stage4.txt": "prompts/stage4.txt"
}

# ✅ Состояния FSM
class PromptEdit(StatesGroup):
    choosing = State()
    editing = State()

# ✅ Команда /edit_prompt или кнопка 📝
@router.message(F.text.in_({"/edit_prompt", "📝 Изменить промт"}))
async def edit_prompt_command(msg: Message, state: FSMContext):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("⛔ Только админ может редактировать промты.")

    kb = InlineKeyboardBuilder()
    for key in PROMPT_PATHS:
        kb.button(text=key, callback_data=key)
    kb.adjust(1)

    await msg.answer("Выбери файл промта для редактирования:", reply_markup=kb.as_markup())
    await state.set_state(PromptEdit.choosing)

# ✅ Обработка нажатия на кнопку выбора файла
@router.callback_query(PromptEdit.choosing)
async def show_current_prompt(callback: CallbackQuery, state: FSMContext):
    file_key = callback.data
    file_path = PROMPT_PATHS.get(file_key)

    if not file_path:
        return await callback.answer("❌ Неизвестный файл.")

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

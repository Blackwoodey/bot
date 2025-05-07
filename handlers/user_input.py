from aiogram import Router, types, F
from aiogram.filters import Command
from datetime import datetime
from services.calculator import calculate_archetypes
from services.textbase import get_text
from services.gpt_core import generate_prophetic_text
from services.logger import save_to_history

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет. Напиши свою дату рождения в формате ДД.ММ.ГГГГ, например:\n\n11.02.1986"
    )

@router.message(F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}$"))
async def date_handler(message: types.Message):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y")
        current_year = datetime.now().year

        if not (1900 <= birth_date.year <= current_year):
            await message.answer("Пожалуйста, укажи реальный год рождения от 1900 до текущего 🗓️")
            return

        core, fear, realization = calculate_archetypes(message.text)

        core_text = get_text("core", core)
        fear_text = get_text("fear", fear)
        realization_text = get_text("realization", realization)

        result = generate_prophetic_text(core_text, fear_text, realization_text)

        save_to_history(core_text, fear_text, realization_text, result)

        await message.answer(result)

    except ValueError:
        await message.answer("Неверный формат даты. Используй ДД.ММ.ГГГГ.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

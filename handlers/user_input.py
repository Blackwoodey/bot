from aiogram import Router, types, F
from datetime import datetime
from aiogram.filters import Command
from services.calculator import calculate_archetypes
from services.textbase import get_text
from services.gpt_core import generate_prophetic_text
from services.logger import save_to_history
from services.detect_theme import detect_theme
from bot import user_context  # ✅ используем общий user_context

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Напиши свою дату рождения в формате ДД.MM.ГГГГ, например:\n\n11.02.1986"
    )

@router.message(F.text.regexp(r"^\d{2}\.\d{2}\.\d{4}$"))
async def date_handler(message: types.Message):
    """
    1-й этап: парсим дату, запускаем finetune-модель и отправляем ОДНО сообщение
    с пророчеством + вопросом в конце.
    """
    user_id = message.from_user.id

    try:
        # 1) Парсим дату
        birth_date = datetime.strptime(message.text, "%d.%m.%Y")
        current_year = datetime.now().year
        if not (1900 <= birth_date.year <= current_year):
            await message.answer("Пожалуйста, укажи реальный год рождения от 1900 до текущего 🗓️")
            return

        # 2) Считаем архетипы
        core, fear, realization = calculate_archetypes(message.text)
        core_text = get_text("core", core)
        fear_text = get_text("fear", fear)
        realization_text = get_text("realization", realization)

        # 3) Генерируем пророческий текст
        result = generate_prophetic_text(core_text, fear_text, realization_text)

        # 4) Сохраняем в историю
        save_to_history(core_text, fear_text, realization_text, result)

        # 5) Отправляем по частям (если длинный)
        MAX_LEN = 4096
        for i in range(0, len(result), MAX_LEN):
            await message.answer(result[i : i + MAX_LEN])

        # 6) Переводим пользователя в стадию 3 (ожидание отклика)
        user_context[user_id] = {
            "state": "awaiting_stage3",
            "birth_date": birth_date,
            "arch": None,
            "theme": None,
            "last_user_message": ""
        }

    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, используй ДД.MM.ГГГГ.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

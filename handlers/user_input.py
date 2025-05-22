from aiogram import Router, types, F
from datetime import datetime
from aiogram.filters import Command
from services.calculator import calculate_archetypes
from services.textbase import get_text
from services.gpt_core import generate_prophetic_text
from services.logger import save_to_history
from handlers.stage2_question import ask_initiation_question
from handlers.stage3_recognition import recognize_arch_state
from handlers.stage3_direction import suggest_path_from_arch
from handlers.stage4_offer import offer_calculation
from services.detect_theme import detect_theme  # ⬅️ Добавлено

router = Router()
user_context = {}

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

        print("\n=== ВХОД В GPT ===")
        print(f"CORE:\n{core_text}\n")
        print(f"FEAR:\n{fear_text}\n")
        print(f"REALIZATION:\n{realization_text}\n")
        print("==================\n")

        result = generate_prophetic_text(core_text, fear_text, realization_text)
        save_to_history(core_text, fear_text, realization_text, result)

        MAX_LEN = 4096
        for i in range(0, len(result), MAX_LEN):
            await message.answer(result[i:i+MAX_LEN])

        stage2_reply = ask_initiation_question(core_text, fear_text, realization_text)
        await message.answer(stage2_reply)

        user_context[message.from_user.id] = {
            "state": "awaiting_stage3",
            "arch": None,
            "theme": None,
            "last_user_message": ""
        }

    except ValueError:
        await message.answer("Неверный формат даты. Используй ДД.ММ.ГГГГ.")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_stages(message: types.Message):
    user_id = message.from_user.id
    context = user_context.get(user_id, {})

    if context.get("state") == "awaiting_stage3":
        arch_result = recognize_arch_state(message.text)
        await message.answer(arch_result)

        known = [
            "Повешенный", "Башня", "Луна", "Дьявол", "Отшельник", "Фортуна", "Смерть",
            "Жрица", "Влюблённые", "Справедливость", "Мир", "Маг", "Звезда"
        ]
        detected = next((a for a in known if a in arch_result), None)
        context["arch"] = detected or "Повешенный"
        context["last_user_message"] = message.text

        direction = suggest_path_from_arch(context["arch"])
        await message.answer(direction)

        context["state"] = "awaiting_stage4"
        user_context[user_id] = context
        return

    if context.get("state") == "awaiting_stage4":
        theme = detect_theme(message.text)
        context["theme"] = theme
        context["last_user_message"] = message.text

        final_reply = offer_calculation(theme, message.text)
        await message.answer(final_reply)

        context["state"] = "awaiting_payment_confirmation"
        user_context[user_id] = context
        return

    if context.get("state") == "awaiting_payment_confirmation":
        agree_words = ["да", "давай", "готов", "хочу", "рассчитать", "согласен", "подходит", "ок"]

        if any(w in message.text.lower() for w in agree_words):
            theme = context.get("theme", "общая")
            payment_message = ""

            if theme == "деньги":
                payment_message = (
                    "🪙 Расчёт “4 = 1” — Инициация на новый денежный уровень\n"
                    "Ты получаешь 4 точных расчёта по дате:\n\n"
                    "— Где перекрыт денежный поток\n"
                    "— Твой архетип бедности и амулет силы\n"
                    "— Архетип долга и ритуал освобождения\n"
                    "— Тень богатства — и как превратить её в силу\n\n"
                    "💰 Стоимость: 890₽ вместо 4900₽\n"
                    "🔗 Для оплаты (Россия): 5536 9140 2191 7509 (Ксения Рузанова)\n"
                    "🌍 Для других стран: https://payform.ru/5e6P2sb\n"
                    "📝 После оплаты: чек, ФИО и дату рождения → @TaroKsenia"
                )
            elif theme == "кризис":
                payment_message = (
                    "⚠️ Расчёт “Выход из кризиса” — 3 сценария выхода из петли\n"
                    "Ты узнаешь:\n"
                    "— Почему именно сейчас застой\n"
                    "— Откуда пришёл удар\n"
                    "— Что за цикл повторяется\n"
                    "— Как выбраться (3 возможных пути)\n\n"
                    "💰 Стоимость: 490₽ вместо 2900₽\n"
                    "🔗 Для оплаты (Россия): 5536 9140 2191 7509 (Ксения Рузанова)\n"
                    "🌍 Для других стран: https://payform.ru/gd7kXZP\n"
                    "📝 После оплаты: чек, ФИО и дату рождения → @TaroKsenia"
                )
            else:
                payment_message = (
                    "🌌 Расчёт “Ядро – Тень – Блок – Переход”\n"
                    "Ты увидишь:\n"
                    "— Твою базовую архетипическую силу (ядро)\n"
                    "— Где ты застрял (тень)\n"
                    "— Что мешает перейти (блок)\n"
                    "— И архетип силы, через который открывается новый путь\n\n"
                    "💰 Стоимость: 490₽ вместо 2900₽\n"
                    "🔗 Для оплаты (Россия): 5536 9140 2191 7509 (Ксения Рузанова)\n"
                    "🌍 Для других стран: https://payform.ru/gd7kXZP\n"
                    "📝 После оплаты: чек, ФИО и дату рождения → @TaroKsenia"
                )

            await message.answer(payment_message)
            context["state"] = "done"
            user_context[user_id] = context

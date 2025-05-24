import openai
import asyncio
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Предварительный вопрос, если нет ответа
fallback_question = "Ты готов услышать — где выход?"

async def suggest_path_from_arch(arch_name: str, user_answer: str = None) -> str:
    try:
        with open("prompts/stage3b.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Если нет ответа от пользователя — возвращаем вопрос
        if not user_answer:
            return fallback_question

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Арахетип: {arch_name}\nОтвет пользователя: {user_answer}"}
            ],
            temperature=1.0,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Ошибка в этапе 3b: {e}]"

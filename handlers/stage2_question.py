import openai
from config import OPENAI_API_KEY

# Устанавливаем API-ключ
openai.api_key = OPENAI_API_KEY

def ask_initiation_question(arch_core: str, arch_fear: str, arch_realization: str) -> str:
    try:
        with open("prompts/stage2.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Вот архетипы по дате рождения: Ядро — {arch_core}, Страх — {arch_fear}, Реализация — {arch_realization}. Что ты скажешь ему первым?"}
            ],
            temperature=1.0,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Ошибка в этапе 2: {e}]"

import os
import openai
from config import OPENAI_API_KEY, OPENAI_MODEL

# Загружаем промт
try:
    with open("prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except Exception as e:
    SYSTEM_PROMPT = "SYSTEM_PROMPT не удалось загрузить: " + str(e)

# Удаляем возможные переменные прокси, чтобы не мешали
for var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
    os.environ.pop(var, None)

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

openai.api_key = OPENAI_API_KEY

# 🔥 Переменная temperature (можно менять через Telegram)
TEMPERATURE_FILE = "temperature.txt"

def get_temperature() -> float:
    try:
        with open(TEMPERATURE_FILE, "r", encoding="utf-8") as f:
            return float(f.read().strip())
    except:
        return 1.0  # значение по умолчанию

def set_temperature(new_temp: float):
    with open(TEMPERATURE_FILE, "w", encoding="utf-8") as f:
        f.write(str(new_temp))

def generate_prophetic_text(core_text: str, fear_text: str, realization_text: str) -> str:
    try:
        temperature = get_temperature()
        user_input = (
            f"Ядро: {core_text}\n\n"
            f"Страх: {fear_text}\n\n"
            f"Реализация: {realization_text}"
        )

        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=temperature,
            max_tokens=2500
        )

        result = response.choices[0].message.content.strip()

        # Если ответ слишком короткий — дополняем
        if len(result.split()) < 250:
            continuation = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": result + "\n\nПродолжи, раскрой глубже, заверши путь до конца."}
                ],
                temperature=temperature,
                max_tokens=1200
            )
            result += "\n\n" + continuation.choices[0].message.content.strip()

        return result

    except Exception as e:
        return f"Ошибка генерации: {e}"

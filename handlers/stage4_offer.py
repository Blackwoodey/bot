from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def offer_calculation(theme: str, user_message: str) -> str:
    try:
        with open("prompts/stage4.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        # Вводим оба параметра в один запрос
        input_text = f"theme: {theme}\n\nuser_message: {user_message}"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ],
            temperature=1.0,
            max_tokens=1200
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Ошибка в этапе 4: {e}]"

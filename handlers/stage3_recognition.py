from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def recognize_arch_state(user_message: str) -> str:
    try:
        with open("prompts/stage3.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=1.0,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Ошибка в этапе 3: {e}]"

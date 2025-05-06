import json
from pathlib import Path

TEXTS_FILE = Path("data/texts.json")

with TEXTS_FILE.open(encoding="utf-8") as f:
    data = json.load(f)

def get_text(category: str, number: int) -> str:
    """Возвращает текст по категории ('core', 'fear', 'realization') и номеру архетипа."""
    return data[category][str(number)]

import json
from pathlib import Path

LOG_PATH = Path("logs/history.jsonl")

def save_to_history(core_text: str, fear_text: str, realization_text: str, result: str):
    entry = {
        "input": {
            "core": core_text,
            "fear": fear_text,
            "realization": realization_text
        },
        "output": result
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

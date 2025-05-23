import re

def detect_theme(text: str) -> str:
    text = text.lower()

    money_patterns = [
        r"\bденьг", r"\bфинанс", r"\bоплат", r"\bплат", r"\bцена", r"\bстоимост",
        r"\bдоход", r"\bзаработ", r"\bбедн", r"\bдолг", r"выживан", r"поток"
    ]

    crisis_patterns = [
        r"\bкризис", r"\bзастой", r"\bперелом", r"\bцикл", r"\bповтор",
        r"\bтупик", r"\bзастрял", r"замкнут", r"ничего не двигается", r"слом"
    ]

    if any(re.search(pat, text) for pat in money_patterns):
        return "деньги"
    elif any(re.search(pat, text) for pat in crisis_patterns):
        return "кризис"
    return "общая"

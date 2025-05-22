def detect_theme(text: str) -> str:
    text = text.lower().strip()

    money_keywords = [
        "деньги", "бедность", "долги", "потолок", "финансы",
        "страх выживания", "нет денег", "хочу денег", "денежный поток"
    ]
    crisis_keywords = [
        "кризис", "застой", "цикл", "повтор", "замкнутый круг", "ничего не двигается"
    ]

    if any(kw in text for kw in money_keywords):
        return "деньги"
    elif any(kw in text for kw in crisis_keywords):
        return "кризис"
    return "общая"

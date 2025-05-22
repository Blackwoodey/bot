def detect_theme(text: str) -> str:
    text = text.lower().strip()

    money_keywords = [
        "деньги", "денег", "деньгам", "финансы", "оплата", "оплатить", "платить",
        "платёж", "цены", "стоимость", "доход", "заработок", "бедность", "долги",
        "страх выживания", "денежный поток"
    ]

    crisis_keywords = [
        "кризис", "застой", "цикл", "повтор", "замкнутый круг", "ничего не двигается",
        "слом", "поворотный момент", "перелом", "тупик", "непонятно", "застрял"
    ]

    if any(kw in text for kw in money_keywords):
        return "деньги"
    elif any(kw in text for kw in crisis_keywords):
        return "кризис"
    return "общая"

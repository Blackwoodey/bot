import re

def detect_theme(text: str) -> str:
    text = text.lower()

    money_patterns = [
        r"деньг", r"финанс", r"оплат", r"плат", r"цена", r"стоимост",
        r"доход", r"заработ", r"бедн", r"долг", r"выживан", r"поток", r"расход"
    ]

    crisis_patterns = [
        r"кризис", r"застой", r"перелом", r"цикл", r"повтор",
        r"тупик", r"застрял", r"замкнут", r"ничего не двигается",
        r"слом", r"разрыв", r"катастроф", r"упадок", r"нестабильн"
    ]

    if any(re.search(pat, text) for pat in money_patterns):
        return "деньги"
    elif any(re.search(pat, text) for pat in crisis_patterns):
        return "кризис"
    return "общая"

def reduce(n):
    while n > 22:
        n -= 22
    return n

def calculate_archetypes(date_str):
    day, month, year = map(int, date_str.strip().split('.'))
    core = reduce(day)
    fear = reduce(day + month)
    realization = reduce(day + month + sum(map(int, str(year))))
    return core, fear, realization

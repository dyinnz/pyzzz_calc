import math


def parse_float(s):
    if s[-1] == "%":
        return float(s[:-1]) / 100
    else:
        return float(s)


def calc_defense(level: int, base: int = 50) -> float:
    if level > 60:
        level = 60
    return math.floor(0.1551 * level * level + 3.141 * level + 47.2049) * base / 50.0

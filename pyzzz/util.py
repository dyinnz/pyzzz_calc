def parse_float(s):
    if s[-1] == "%":
        return float(s[:-1]) / 100
    else:
        return float(s)

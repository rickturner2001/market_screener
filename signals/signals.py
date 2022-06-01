def adr_signals_long(adr: float, close: float, ma100: float, ma20: float) -> bool:
    if (adr >= 2) and (close > ma100) and (close < ma20):
        return True
    return False


def adr_signals_short(adr: float, close: float, ma100: float, ma20: float) -> bool:
    if (adr <= .5) and (close < ma100) and (close > ma20):
        return True
    return False

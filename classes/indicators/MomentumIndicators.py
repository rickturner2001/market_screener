from dataclasses import dataclass
import pandas as pd
import numpy as np
from pandas import Series


@dataclass
class RSI:
    closes: Series
    period: int = 14

    def __post_init__(self) -> None:
        self.data: Series = self.get_rsi()

    def get_rsi(self) -> Series:
        delta = self.closes.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=self.period - 1 if self.period > 0 else 0, adjust=False).mean()
        ema_down = down.ewm(com=self.period - 1 if self.period > 0 else 0, adjust=False).mean()
        rs = ema_up / ema_down
        rsi = 100 - (100 / (1 + rs))
        rsi[:15] = None
        return rsi


@dataclass
class MACD:
    adj_closes: Series
    slow_length: int = 26
    fast_length: int = 12
    signal_smoothing: int = 9

    def __post_init__(self):
        self.data = self.get_macd()

    def get_macd(self):
        fast_ema = self.adj_closes.ewm(span=self.fast_length).mean()
        slow_ema = self.adj_closes.ewm(span=self.slow_length).mean()
        macd = (slow_ema - fast_ema) * -1
        macd_signal_line = macd.ewm(span=self.signal_smoothing).mean()
        histogram = macd - macd_signal_line
        return macd, macd_signal_line, histogram


def get_atr(df: pd.DataFrame) -> Series:
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(14).sum() / 14
    return atr


def get_tr(high, low, previous_close):
    return max([(high - low), abs(high - previous_close), abs(low - previous_close)])


def get_p_dm(high, previous_high):
    return high - previous_high


def get_n_dm(low, previous_low):
    return previous_low - low


def get_dm(p_dm, n_dm):
    dm = p_dm if (p_dm >= n_dm) else n_dm


def get_p_di(smoothed, atr, dm):
    return ((smoothed + dm) / atr) * 100


def get_n_di(smoothed, atr, dm):
    return ((smoothed - dm) / atr) * 100


def get_dx(p_di, n_di):
    return (abs(p_di - n_di) / abs(p_di + n_di)) * 100


def get_adx(dx_14, period, size):
    adx = np.empty(size)
    for i in range(size):
        if i >= period:
            pass
        else:
            if not adx[-1] > 0:
                adx[i] = dx_14[i]
            else:
                adx[i] = ((adx[-1] * (period - 1)) + dx_14[i]) / period

    return adx


def get_adx(high, previous_high, low, previous_low, atr, tr, period):
    p_dm = high - previous_high
    n_dm = previous_low - low

    dm = get_dm(p_dm, n_dm)
    dm_14 = dm.rolling(windo=period).mean()

    smoothed = dm_14 - (dm_14 / period) + dm



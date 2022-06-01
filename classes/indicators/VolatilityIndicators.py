from dataclasses import dataclass
from pandas import Series


@dataclass
class Bollinger:
    closes: Series
    lows: Series
    highs: Series
    period: int = 20
    std_dev: int = 2
    offset: float = 0

    def __post_init__(self) -> None:
        self.data = self.get_bollinger()

    def get_bollinger(self) -> tuple:
        typical_price = (self.closes + self.lows + self.highs) / 3
        std = typical_price.rolling(self.period).std(ddof=self.offset)
        middle = typical_price.rolling(self.period).mean()
        upper = middle + self.std_dev * std
        lower = middle - self.std_dev * std

        return lower, middle, upper


@dataclass
class Stochastic:
    closes: Series
    highs: Series
    lows: Series
    k_period: int = 14
    d_period: int = 3

    def __post_init__(self) -> None:
        self.data = self.get_stochastic()

    def get_stochastic(self) -> tuple:
        self.highs = self.highs.rolling(self.k_period).max()
        self.lows = self.lows.rolling(self.k_period).min()
        stoch_k = (self.closes - self.lows) * 100 / (self.highs - self.lows)
        stoch_d = stoch_k.rolling(self.d_period).mean()
        return stoch_k, stoch_d

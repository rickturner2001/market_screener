from enum import Enum


class ActiveStrategies(Enum):
    # Single
    ICHIMOKU = 1
    SOF = 2
    OVERSOLD_STOCHASTIC = 3
    OVERSOLD_MACD = 4

    # Double
    ICHIMOKU_SOF = 5
    ICHIMOKU_OVERSOLD_STOCH = 6
    ICHIMOKU_OVERSOLD_MACD = 7
    OVERSOLD_MACD_SOF = 8
    OVERSOLD_STOCH_SOF = 9
    OVERSOLD_STOCH_MACD = 10

    # Triple
    ICHIMOKU_SOF_STOCH = 11
    SOF_STOCH_MACD = 12
    ICHIMOKU_SOF_MACD = 13
    ICHIMOKU_STOCH_MACD = 14

    # Full
    FULL_COMBO = 15

"""
Investopedia 2022, https://www.investopedia.com/terms/m/market_breadth.asp

 Market breadth refers to how many stocks are participating in a given move in an index or on a stock exchange.
 An index may be rising yet more than half the stocks in the index are falling because a small number of stocks
 have such large gains that they drag the whole index higher.

Market breadth indicators can reveal this and warn traders that most stocks are not actually performing well,
even though the rising index makes it look like most stocks are doing well—an index is an average of the stocks in it.
Volume may also be added into these indicator calculations to provide additional insight into how stocks within an index
are acting overall.
"""

from typing import Union, List

from pandas import DataFrame
from classes.database.Database import Database
from abc import abstractmethod


class MarketBreadthAnalysis:

    @staticmethod
    def new_highs_lows_index(market_data: DataFrame) -> bool:
        """compares stocks making 52-week highs to stocks making 52-week lows"""
        ...

    @staticmethod
    def ad_ratio_value(database: Database) -> List[Union[int, float]]:
        # TODO (maybe doesn't belong here)
        """The advance decline ratio (ADR) is a technical indicator used to assess stock market sentiment. The ratio
        compares the number of stocks that increased in value to the number of stocks that decreased in value. In
        other words, the ADR compares the number of stocks that rose in price versus the number of stocks that
        declined in price. """
        pass

    @staticmethod
    def on_balance_volume_indicator(dataframe: DataFrame) -> List[Union[float, int]]:
        """
        looks at volume, except up or down volume is based on whether the index rises or falls. If the index falls,
        the total volume is counted as negative. If the index rises, the total volume is negative
        """
        obv = []
        for i, date in enumerate(dataframe.index):
            previous_obv = None if not len(obv) else obv[-1]
            obv.append(
                MarketBreadthAnalysis.on_balance_volume(previous_obv, dataframe['Volume'].iloc[i],
                                                        dataframe['Close'].iloc[i], dataframe['Close'].iloc[i - 1]))
        return obv

    @staticmethod
    def sefi(self):
        pass

    @staticmethod
    def on_balance_volume(
            previous_obv: Union[float, int], volume: int, close: Union[float, int],
            previous_close: Union[float, int]) -> Union[float, int]:

        if not previous_obv:
            return volume

        if close > previous_close:
            return previous_obv + volume

        elif close < previous_close:
            return previous_obv - volume

        return previous_obv

    def count_volume_change(self, date: str, positive: bool = True) -> int:
        pass

    @abstractmethod
    def advancing_volume_index(self) -> List[int]:
        pass

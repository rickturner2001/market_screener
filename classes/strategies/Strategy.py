from abc import ABC, abstractmethod
from typing import List

from pandas import DataFrame


class Strategy(ABC):
    """Abstract class representation of a single strategy"""

    def __init__(self, dataframe: DataFrame):
        self.dataframe = dataframe

    @abstractmethod
    def apply(self) -> List[str]:
        """
        Method that executes a specific strategy given the market data
        :return: list of tickers where the strategy might be effective
        """
        pass

from pandas import DataFrame


class SP500MarketData:
    """Class that contains the methods to organize SP100 market data"""

    @staticmethod
    def evaluate_change_by_day(dataframe: DataFrame) -> bool:
        """Takes in a dataframe and returns True if more than 50% of the tickers have a positive change"""
        if len(dataframe[dataframe['change'] > 0]) > len(dataframe) / 2:
            return True
        return False

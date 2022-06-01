from dataclasses import dataclass
from typing import Union, List

import numpy as np
from pandas import Series, DataFrame
from classes.database.SP500Database import SP500Database


@dataclass
class MovingAverages:
    closes: Series

    @property
    def ma_20(self):
        return self.closes.rolling(window=20).mean()

    @property
    def ma_50(self):
        return self.closes.rolling(window=50).mean()

    @property
    def ma_100(self):
        return self.closes.rolling(window=100).mean()

    @property
    def ma_200(self):
        return self.closes.rolling(window=200).mean()


@dataclass
class Sefi:
    close: list
    ma20: list

    def __post_init__(self) -> None:
        self.data = self.get_sefi()

    def get_sefi(self) -> list:
        return [self.evaluate(close, ma20) for close, ma20 in zip(self.close, self.ma20)]

    @staticmethod
    def evaluate(close: float, ma20: float) -> Union[float, int]:
        return 1 if close > ma20 else 0


# MARKETS ONLY
class ADR:
    def __init__(self, market_data: SP500Database):
        self.market_data = market_data

    def ad_ratio_value(self) -> List[Union[int, float]]:
        dates = self.market_data.query_all_dates()
        values = []
        for date in dates:
            dataframe = self.market_data.query_from_date_to_dataframe(date)

            # TODO division by 0
            values.append(len(dataframe[dataframe['Change'] > 0]) / len(dataframe[dataframe['Change'] <= 0]))
        return values

    @property
    def data(self):
        return self.ad_ratio_value()


class CVI:
    def __init__(self, market_data: SP500Database):
        self.market_data = market_data

    def advancing_volume_index(self) -> List[int]:
        dates = self.market_data.query_all_dates()
        return [self.count_volume_change(date) - self.count_volume_change(date, positive=False) for date in dates]

    def count_volume_change(self, date: str, positive: bool = True) -> int:
        return self.market_data.cursor.execute(
            f"""select count(Volume_Change) from historical_data
                where date = '{date}' and volume_change {'>' if positive else '<'} 0""").fetchone()['count('
                                                                                                    'Volume_Change)']

    def cumulative_volume_index(self):
        return np.array(self.advancing_volume_index()).cumsum()

    @property
    def data(self):
        return self.cumulative_volume_index()


def inject_ichimoku(dataframe: DataFrame):
    nine_period_high = dataframe['High'].rolling(window=9).max()
    nine_period_low = dataframe['Low'].rolling(window=9).min()

    dataframe['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

    period26_high = dataframe['High'].rolling(window=26).max()
    period26_low = dataframe['Low'].rolling(window=26).min()

    dataframe['kijun_sen'] = (period26_high + period26_low) / 2
    dataframe['senkou_span_a'] = ((dataframe['tenkan_sen'] + dataframe['kijun_sen']) / 2).shift(26)

    period52_high = dataframe['High'].rolling(window=52).max()
    period52_low = dataframe['Low'].rolling(window=52).min()

    dataframe['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

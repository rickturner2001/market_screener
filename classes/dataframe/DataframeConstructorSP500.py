from dataclasses import dataclass
import numpy as np
from pandas import DataFrame

from classes.database.SP500Database import SP500Database
from classes.dataframe.DataframeConstructor import DataframeConstructor


@dataclass
class DataframeConstructorSP500(DataframeConstructor):

    def construct_df(self, ticker: str) -> DataFrame:
        data = self.database.query_ticker_data(ticker)
        dict_df = {}

        for column in SP500Database.columns:
            # dict_df[column] = np.array([])
            dict_df[column] = np.array([], dtype=np.dtype("float64"))
            for i, _ in enumerate(data):
                np.append(dict_df[column], (data[i][column]))

        return DataFrame.from_dict(dict_df)

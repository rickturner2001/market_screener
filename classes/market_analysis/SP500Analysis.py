import numpy as np
from numpy import array as np_array
from classes.database.SP500Database import SP500Database
from classes.indicators.MiscIndicators import Sefi
from classes.market_analysis.MarketBreadthAnalysis import MarketBreadthAnalysis
from classes.tickersdata.GeneralMarketDataFetcher import GeneralMarketDataFetcher
from classes.dataframe.EnhancedDataframe import EnhancedDataframe
from classes.indicators.MiscIndicators import ADR
from signals.signals import adr_signals_long, adr_signals_short
from pandas import DataFrame
import datetime

current_date = datetime.date.today()
one_year_ago = datetime.date.today() - datetime.timedelta(days=365)


class SP500Analysis(MarketBreadthAnalysis):

    def __init__(self, market_data: SP500Database):
        self.sp500: DataFrame = None
        self.dates = None
        self.market_data = market_data

    def sefi(self, ma_column='MA20') -> DataFrame:
        self.dates = self.market_data.query_all_dates()

        self.sp500 = GeneralMarketDataFetcher.oex_download_data(start=one_year_ago, end=current_date)
        self.sp500 = EnhancedDataframe.populate_dataframe(self.sp500, "SPX")
        self.sp500['Change'] = (self.sp500['Close'].pct_change(1) * 100).cumsum()

        # TODO looks like shit refactor this code ASAP
        results = []
        for date in self.dates:
            dataframe = self.market_data.query_from_date_to_dataframe(date)
            dataframe['SEFI'] = Sefi(dataframe['Close'], dataframe[ma_column]).data
            results.append(len(dataframe[dataframe["SEFI"] == 0]) / len(dataframe))

        if not len(self.sp500) == len(results):
            results = results[-len(self.sp500):]

        self.sp500['SEFI'] = np_array(results) * 100

        def sefi_signal_long(sefi):
            if sefi >= 75:
                return True
            return False

        def sefi_signal_short(sefi):
            if sefi <= 25:
                return True
            return False

        self.sp500['SEFI Signal Long'] = np.vectorize(sefi_signal_long)(self.sp500["SEFI"])

        self.sp500["SEFI Signal Short"] = np.vectorize(sefi_signal_short)(self.sp500['SEFI'])
        return self.sp500

    def adr_analysis(self) -> DataFrame:
        if not self.dates:
            self.dates = self.market_data.query_all_dates()

        adr = ADR(market_data=self.market_data)
        # TODO
        # if self.sp500 == None:
        #     self.sp500 = GeneralMarketDataFetcher().oex_download_data(start=self.dates[0], end=self.dates[-1])
        #     self.sp500 = EnhancedDataframe.populate_dataframe(self.sp500)

        self.sp500.rename(columns={"Adjusted Close": "Adjusted_Close"}, inplace=True)
        adr_data = adr.data
        if not len(self.sp500) == len(adr_data):
            adr_data = adr_data[-len(self.sp500):]
        self.sp500["ADR"] = adr_data
        self.sp500['ADR Signal Long'] = np.vectorize(adr_signals_long)(self.sp500["ADR"], self.sp500['Close'],
                                                                       self.sp500["MA100"], self.sp500["MA20"])
        self.sp500['ADR Signal Short'] = np.vectorize(adr_signals_short)(self.sp500["ADR"], self.sp500['Close'],
                                                                         self.sp500["MA100"], self.sp500["MA20"])

        return self.sp500

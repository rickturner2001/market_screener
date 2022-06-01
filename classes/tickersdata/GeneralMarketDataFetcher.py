from dataclasses import dataclass
from typing import List

from pandas import read_csv, DataFrame
from pandas_datareader.yahoo.daily import YahooDailyReader
from yfinance import download

from config import file_path


@dataclass
class GeneralMarketDataFetcher:

    def download_data(self, period: str = "1y", interval: str = "1d") -> DataFrame:
        tickers_data = download(
            tickers=self.tickers, period=period, interval=interval, group_by='ticker', auto_adjust=False,
            prepost=False, threads=True, proxy=None)

        tickers_data = tickers_data.T
        return tickers_data

    @property
    def tickers(self) -> List[str]:
        tickers_table = read_csv(file_path / "sp500.csv")
        tickers = [ticker if "." not in ticker else ticker.replace(".", "-") for ticker in tickers_table['Symbol']]
        return tickers

    @staticmethod
    def single_ticker_download(ticker, period, interval):
        download(ticker, period=period, interval=interval)

    @staticmethod
    def oex_download_data(start, end) -> DataFrame:
        dataframe = YahooDailyReader(symbols="^GSPC", start=start, end=end).read()
        return dataframe

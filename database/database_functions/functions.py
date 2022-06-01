from pathlib import Path
from typing import Union
import colorama
from classes.database.SP500Database import SP500Database
from classes.dataframe.EnhancedDataframe import EnhancedDataframe
from classes.tickersdata.GeneralMarketDataFetcher import GeneralMarketDataFetcher
from config import db_path
from cython import cfunc


def create_database_sp500(filename: str, extension: str, database_dir: Union[Path, str] = db_path) -> SP500Database:
    database = SP500Database()
    database.create_database_file(path=database_dir, filename=filename, extension=extension)
    database.establish_connection()
    database.create_table_historical()
    return database


@cfunc
def populate_sp500(database: SP500Database, verbose: bool = True, update: bool = True) -> None:
    """
     Populates SP500 database with (OHLCV, adj close, and indicators )

    :param database: database to be updated
    :param verbose: shows progress in % if set to True
    :param update: updates only last day if set to True
    """
    sp100_historical = GeneralMarketDataFetcher()
    tickers = sp100_historical.tickers

    if update:
        tickers_data = sp100_historical.download_data(period='1d', interval='1d')
        # database.update_db()
    else:
        database.clear_historical()
        print(f"Cleared {database.historical_tablename} table")
        tickers_data = sp100_historical.download_data()

    for n, ticker in enumerate(tickers):
        percent = 100 * (n / float(len(tickers)))
        bar = "█" * int(percent) + '-' * (100 - int(percent))
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")
        if n == len(ticker):
            print(colorama.Fore.CYAN + f"\r|{bar}| {percent:.2f}%", end="\r")

        df = tickers_data.loc[ticker].T
        df = EnhancedDataframe.populate_dataframe(df, ticker)
        database.do_populate(df)

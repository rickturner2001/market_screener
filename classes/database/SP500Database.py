import sqlite3
from dataclasses import dataclass
from sqlite3 import Row
from typing import Union, List, Iterator

from pandas import read_sql, DataFrame
import numpy as np
from classes.database.Database import Database
from classes.tickersdata.GeneralMarketDataFetcher import GeneralMarketDataFetcher
from classes.database.Column import FloatColumn, IntegerColumn, TextColumn
from cython import cfunc
import json

numeric = Union[int, float]


# TODO Optimize function parameters (*args, **kwargs)

@dataclass
class SP500Database(Database):
    _historical_tablename: str = "historical_data"
    _api_data_tablename: str = "api_data"
    _oex_data: str = "sp500_prices"

    columns = np.array(["Date", "Ticker", 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'MA20', 'MA50',
                        'MA100', 'RSI', 'MACD_histogram', 'BB_lower',
                        'BB_middle', 'BB_upper', 'STOCH_K', 'STOCH_D', 'Volume_Change',
                        'Change', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b',
                        ], dtype=np.dtype("U25"))

    int_cols = ['Volume']
    str_cols = ['Date', "Ticker"]

    tickers = GeneralMarketDataFetcher.tickers

    def change_default_historical_table_name(self, table_name: str):
        self._historical_tablename = table_name

    def create_table_historical(self) -> None:
        columns = [IntegerColumn(col) if col in self.int_cols else TextColumn(col) if
        col in self.str_cols else FloatColumn(col) for col in self.columns]

        stmt = SP500Database.create_table(self._historical_tablename, columns,
                                          pk=(IntegerColumn("test", attribute="primary_key", nullable=True)))

        self._cursor.execute(stmt)
        self._connection.commit()
        self._tablenames.append(self._historical_tablename)

    def create_table_api_data(self):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self._api_data_tablename} (id INTEGER PRIMARY KEY, Datetime TEXT, Data STRING)")
        self.connection.commit()

    @cfunc
    def do_populate(self, dataframe: DataFrame):
        """
        Populates the tables containing historical data
        :param dataframe: Pandas dataframe with columns = args
        """
        dataframe.to_sql(self._historical_tablename, self._connection, if_exists="append")
        self._connection.commit()

    def query_ticker_data(self, ticker: str) -> Iterator[DataFrame] or DataFrame:
        return read_sql(f"SELECT * FROM {self._historical_tablename} WHERE ticker = '{ticker}'", self._connection)

    def initial_date(self):
        beginning_date = self._cursor.execute(
            f"""SELECT date from {self._historical_tablename}
                                                WHERE ticker = 'AAPL'"""
        ).fetchone()
        beginning_date = beginning_date['date']
        print(beginning_date)
        return beginning_date

    def clear_historical(self):
        self._cursor.execute(f"delete from {self._historical_tablename}")
        self._connection.commit()

    # def update_db(self):
    #     self._cursor.execute(
    #         f"""DELETE FROM {self._historical_tablename}
    #                             WHERE date = ?
    #                             """, (self.initial_date()))

    @property
    def historical_tablename(self):
        return self._historical_tablename

    def query_data_by_date(self, date: str) -> List[Row]:
        data = self._cursor.execute(f"""
                                      SELECT * from {self._historical_tablename}
                                      WHERE date = ?
                                      """, (date,)).fetchall()
        return data

    def query_by_id(self) -> List[Row]:
        return self._cursor.execute(f"SELECT * from {self._historical_tablename} where id < 10").fetchall()

    def stmt_query_by_date(self, date: str) -> str:
        return f"SELECT * FROM {self._historical_tablename} WHERE date = '{date}'"

    def query_from_date_to_dataframe(self, date: str) -> DataFrame:
        """Build a dataframe from sql query for data on a give date"""
        return read_sql(self.stmt_query_by_date(date), self._connection)

    def query_all_dates(self) -> List[str]:
        dates = self._cursor.execute(f"SELECT DISTINCT (date) FROM {self._historical_tablename}").fetchall()
        return [date['date'] for date in dates]

    def get_latest_date(self) -> str:
        date = self._cursor.execute(f"""
                                        SELECT DISTINCT (date) from {self._historical_tablename}
                                        ORDER BY date DESC LIMIT 1
                                    """).fetchone()
        return date['date']

    def get_date_before_latest_date(self) -> str:
        date = self._cursor.execute(f"""
                                        SELECT DISTINCT (date) from {self._historical_tablename}
                                        ORDER BY date DESC LIMIT 2
                                    """).fetchall()
        return date[-1]['date']

    def query_breadth_specifics(self) -> tuple:
        last_date = self.query_all_dates()[-1]
        changes = self.cursor.execute \
            (f"SELECT * FROM {self._historical_tablename} WHERE Date = ?", (last_date,)).fetchall()

        def parse_query(query, colname: str):
            return [(val['Ticker'], val[colname]) for val in query]

        return parse_query(changes, "Change"), parse_query(changes, "Volume_Change")

    def get_last_api_request(self):
        data = self.cursor.execute(f"SELECT * FROM {self._api_data_tablename} ORDER BY id DESC LIMIT 1").fetchone()
        return data

    def insert_api_data(self, datetime, data):
        data = json.dumps(data)
        print("Adding to Table")
        self.cursor.execute(f"INSERT INTO {self._api_data_tablename} (Datetime, Data) VALUES (?, ?)", (datetime, data))
        self.connection.commit()

import json
import sqlite3
import sys

from config import db_path, file_path
from sqlalchemy.orm import Session
from sqlalchemy import engine
from api_database import APIEntries, TickerEntry
import pandas as pd
from enums import ActiveStrategies
from statements import get_success_rate_for_n_days_holding

TICKERS_FILE_DATA = pd.read_csv(file_path / "sp500.csv")
TICKERS_FILE_DATA.index = TICKERS_FILE_DATA['Symbol']


def register_entries(data: tuple) -> None:
    date, entries, sefi, adr = data
    with Session(engine) as session:
        session.add(
            APIEntries(
                date=date,
                entries=entries,
                adr=adr,
                sefi=sefi
            )
        )

        session.commit()


def register_single_entry(data: tuple) -> None:
    parent_id, ticker, entry, sector = data
    with Session(engine) as session:
        session.add(
            TickerEntry(
                ticker=ticker,
                sector=sector,
                entry=entry,
                parent_entry_id=parent_id
            )
        )
        session.commit()


def get_all_entries():
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    data = cursor.execute("SELECT * FROM api_entries WHERE entries").fetchall()
    return data


def get_api_data_from_date(date):
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    data = cursor.execute(
        """ 
        SELECT api_entries.id, date, data FROM api_data_tester join api_entries
        on api_entries.date = api_data_tester.Datetime where api_entries.entries
        and api_entries.date = ?
        """, (date,)).fetchone()
    return data


def check_indicator_status(dictionary, strategy):
    return dictionary[strategy]['status']


def define_entry(entry_data, tickers):
    ticker_entries = []
    for ticker in tickers:
        ticker_data = entry_data[ticker]
        if ticker_data["Ichimoku"]['status'] and ticker_data["oversold_slow_over_fast"]['status'] \
                and ticker_data["oversold_stochastic"]['status'] and ticker_data["oversold_MACD"]['status']:
            ticker_entries.append(ActiveStrategies.FULL_COMBO.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_slow_over_fast']['status'] and \
                ticker_data["oversold_stochastic"]['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_SOF_STOCH.value)
        elif ticker_data['oversold_slow_over_fast']['status'] and ticker_data["oversold_stochastic"]['status'] and \
                ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.SOF_STOCH_MACD.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_slow_over_fast']['status'] and \
                ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_SOF_MACD.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_stochastic']['status'] and \
                ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_STOCH_MACD.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_slow_over_fast']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_SOF.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_stochastic']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_OVERSOLD_STOCH.value)
        elif ticker_data['Ichimoku']['status'] and ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU_OVERSOLD_MACD.value)
        elif ticker_data['oversold_MACD']['status'] and ticker_data['oversold_slow_over_fast']['status']:
            ticker_entries.append(ActiveStrategies.OVERSOLD_MACD_SOF.value)
        elif ticker_data['oversold_stochastic']['status'] and ticker_data['oversold_slow_over_fast']['status']:
            ticker_entries.append(ActiveStrategies.OVERSOLD_STOCH_SOF.value)
        elif ticker_data['oversold_stochastic']['status'] and ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.OVERSOLD_STOCH_MACD.value)
        elif ticker_data['Ichimoku']['status']:
            ticker_entries.append(ActiveStrategies.ICHIMOKU.value)
        elif ticker_data['oversold_slow_over_fast']['status']:
            ticker_entries.append(ActiveStrategies.SOF.value)
        elif ticker_data['oversold_stochastic']['status']:
            ticker_entries.append(ActiveStrategies.OVERSOLD_STOCHASTIC.value)
        elif ticker_data['oversold_MACD']['status']:
            ticker_entries.append(ActiveStrategies.OVERSOLD_MACD.value)
        else:
            ticker_entries.append(0)

    return ticker_entries


def parse_single_entry_data(entry_data):
    entries_data = json.loads(entry_data['Data'])['entries']
    tickers = list(entries_data.keys())
    entries_numbers = define_entry(entries_data, tickers)
    parent_id = [entry_data['id'] for _ in range(len(tickers))]
    return tickers, entries_numbers, parent_id


def insert_single_entry_data(entry_data):
    print("Adding Entry")
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    tickers, strategies, parents_id = entry_data
    print("Working with data of length: ", len(tickers))
    i = None
    sectors = [TICKERS_FILE_DATA.loc[ticker.replace("-", ".")]['GICS Sector'] for ticker in tickers]
    for i, _ in enumerate(tickers):
        cursor.execute("INSERT INTO entry (ticker, sector, entry, parent_entry_id) VALUES (?, ?, ?, ?)",
                       (
                           tickers[i],
                           sectors[i],
                           strategies[i],
                           parents_id[i]))

    connection.commit()
    connection.close()


def create_results_table():
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    data = cursor.execute(
        """
        CREATE TABLE api_results as SELECT entry.ticker, entry.entry, entry.sector, api_entries.date, historical_data.change  FROM entry
        INNER JOIN api_entries ON api_entries.id = entry.parent_entry_id INNER JOIN historical_data
        ON historical_data.Ticker = entry.ticker WHERE historical_data.Date = api_entries.date
        """).fetchall()
    return data


def query_all_api_results():
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select ticker, entry, sector, date, Change from api_results")


def query_success_rate_by_days(n_days=20):
    connection = sqlite3.connect(db_path / "sp500.sqlite")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    return cursor.execute(get_success_rate_for_n_days_holding(n_days)).fetchone()

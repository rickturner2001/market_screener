import json
import sys
import numpy as np
from classes.database.SP500Database import SP500Database
from classes.market_analysis.SP500Analysis import SP500Analysis
from classes.strategies.TickerStrategy import TickerStrategy
from config import db_path
import sqlite3
from api_data import parse_entries, get_entries_from_indicators, \
    get_market_breadth_status, plotting_data_breadth
from interactions import register_entries, get_api_data_from_date, get_all_entries, parse_single_entry_data, \
    insert_single_entry_data, query_success_rate_by_days


def do_request_and_add_to_db(data: dict, date: str) -> None:
    try:
        connection = sqlite3.connect(db_path / "sp500.sqlite")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO api_data_tester (Datetime, Data) VALUES (?, ?)",
                       (date, json.dumps(data)))

        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        sys.exit()


def market_status_to_dict_tesing() -> None:
    sp500_database = SP500Database()
    sp500_database.connect_existing_database(db_path / "sp500.sqlite")
    market_analysis = SP500Analysis(sp500_database)
    market_analysis.sefi()
    market_analysis.adr_analysis()
    dates = sp500_database.query_all_dates()
    for i, date in enumerate(dates):
        df = sp500_database.query_from_date_to_dataframe(date)
        entries = get_entries_from_indicators(df)
        entries = parse_entries(entries)

        data = {"market_breadth": {
            'is_entry': bool(get_market_breadth_status(market_analysis)),
            "SEFI": {
                "value": market_analysis.sp500['SEFI'].iloc[i],
                "short": bool(market_analysis.sp500['SEFI Signal Short'].iloc[i]),
                "long": bool(market_analysis.sp500['SEFI Signal Long'].iloc[i])
            },

            "ADR": {
                "value": market_analysis.sp500['ADR'].iloc[i],
                "short": bool(market_analysis.sp500['ADR Signal Short'].iloc[i]),
                "long": bool(market_analysis.sp500['ADR Signal Long'].iloc[i]),
            },

            "strategies": {
                "good_SEFI_oversold": bool(
                    np.vectorize(TickerStrategy.good_sefi_oversold)(market_analysis.sp500['SEFI'],
                                                                    market_analysis.sp500['RSI'],
                                                                    market_analysis.sp500[
                                                                        'BB_lower'],
                                                                    market_analysis.sp500['Close'])[
                        i])
            }

        }, 'entries': entries,

            "plotting": {
                # "entries": plotting_data(sp500_database, [ticker for ticker in entries])
                "breadth": plotting_data_breadth(sp500_database)
            }

        }
        print("Parsing data for date: " + str(date))

        do_request_and_add_to_db(data, date)


def adjust_multiple_entries(data) -> tuple:
    date = data['Datetime']
    data = json.loads(data['data'])
    entries = True if data['entries'] else False
    sefi = 1 if data['market_breadth']['SEFI']['long'] else -1 if data['market_breadth']['SEFI'][
        'short'] else 0
    adr = 1 if data['market_breadth']['ADR']['long'] else -1 if data['market_breadth']['ADR'][
        'short'] else 0
    return date, entries, sefi, adr


def api_testing_data_to_entries():
    sp500_database = SP500Database()
    sp500_database.connect_existing_database(db_path / "sp500.sqlite")
    data = sp500_database.query_all_testing_data()
    for val in data:
        register_entries(adjust_multiple_entries(val))


def parse_entry(data):
    dates = [d['date'] for d in data]
    return dates


def populate_entry_db():
    dates = parse_entry(get_all_entries())
    for date in dates:
        entry_data = get_api_data_from_date(date)
        single_entry_data = parse_single_entry_data(entry_data)
        insert_single_entry_data(single_entry_data)


populate_entry_db()

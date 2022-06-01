from classes.database import SP500Database
from classes import GeneralMarketDataFetcher
from classes import SP500Analysis

# Database init
sp500 = SP500Database()
sp500.connect_existing_database("test.pyx")

# SP500 Dataframe
dates = sp500.query_all_dates()
sp500_dataframe = GeneralMarketDataFetcher().oex_download_data(start=dates[0], end=dates[-1])

# Market analysis
market_breadth_analysis = SP500Analysis(sp500)

avi = market_breadth_analysis.advancing_volume_index()
print(avi)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8), dpi=200)

plt.plot(sp500.query_all_dates(), avi, label="AVI")
plt.legend()
plt.grid()

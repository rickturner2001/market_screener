
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/rickturner2001/SP100_screener/main)   ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/rickturner2001/SP100_screener)    ![GitHub](https://img.shields.io/github/license/rickturner2001/SP100_screener)    ![GitHub top language](https://img.shields.io/github/languages/top/rickturner2001/SP100_screener)    ![GitHub last commit](https://img.shields.io/github/last-commit/rickturner2001/SP100_screener)

# SP100 Screener

We are working on developing a screener aid software with the intent to assist in the making of successful trades.
We intend to do that by using a mix of existing indicators and strategies combined with a series of indicators and techniques developed and backtested by us.

By default, this tool uses the SP100 as its market of choice. It will download the data available from x date to y with a z interval; If not defined, it will download the data (OHLCV) for the last two years with an interval of one day.
The prices are downloaded for every ticker in the SP100 and stored in a database that will be updated daily.

The direct function of this script is to analyze and give out an entry signal with the suggested holding time and the expected percent change in return. 

A series of tests and analyses will  define if the market is in a suitable state, thus ensuring the appropriate conditions to run one or more of the chosen strategies

## More

This project is a work in progress, and the main idea is to develop a desktop app or a web app.

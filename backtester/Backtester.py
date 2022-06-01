import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


class Backtester:
    def __init__(self, entries: list, benchmark: pd.DataFrame, limit=None):
        self.results = None
        self.entries = entries
        self.benchmark = benchmark
        self.benchmark['Change'] = self.benchmark['Close'].pct_change() * 100
        self.benchmark['Cum_change'] = self.benchmark['Change'].cumsum()
        self.limit = limit
        self._sell_points = []

    @property
    def sell_points(self):
        return self._sell_points

    @staticmethod
    def meet_limit_expectation(change, limit):
        return change >= limit

    def eval_position(self, position: str):
        entry_price = self.benchmark['Close'].loc[position]

        negative_changes = list(filter(lambda x: x >= 100, self.benchmark['Cum_change']))
        if any(negative_changes):
            exit = [i for i, _ in enumerate(negative_changes) if i >= 100][0]
            self._sell_points.append(self.benchmark.index[exit])
            exit_price = self.benchmark['Close'].iloc[exit]

            return ((exit_price - entry_price) / exit_price) * 100

        if not self.limit:
            exit_price = self.benchmark['Close'].iloc[-1]
            self._sell_points.append(self.benchmark.index[-1])
            return ((exit_price - entry_price) / exit_price) * 100
        else:

            df = self.benchmark[position:]
            df['Cum_change'] = (df['Close'].pct_change() * 100).cumsum()
            df['exit_points'] = np.vectorize(self.limit['func'])(df[self.limit["colname"]])
            exits = df[df['exit_points']]

            if len(exits) > 0:
                exit_price = self.benchmark['Close'].loc[exits.index[0]]
                self._sell_points.append(exits.index[0])
            else:
                exit_price = self.benchmark['Close'].iloc[-1]
                self._sell_points.append(self.benchmark.index[-1])

        return ((exit_price - entry_price) / exit_price) * 100

    def get_holding_times(self):
        trades = list(zip(self.entries, self.sell_points))
        holding_times = []
        for entry, exits in trades:
            holding_times.append(len(self.benchmark[entry:exits]))

        holding_times = np.array(holding_times)
        maxim = np.max(holding_times)
        minim = np.min(holding_times)
        mean = holding_times.mean()
        return maxim, minim, mean

    def evaluate_strategy(self):
        results = list(map(self.eval_position, self.entries))
        results = np.array(results, dtype=np.dtype("float32"))
        maxim, minim, mean = self.get_holding_times()

        self.results = {
            "returns": results,
            "max": np.max(results),
            "min": np.min(results),
            "mean": results.mean(),
            "std": results.std(),
            "total": results.sum(),
            "entries": len(self.entries),
            "mean_holding_time": mean,
            "max_holding_time": maxim,
            "min_holding_time": minim,
        }

    def pretty_print_results(self):
        print(f"Total Entries: {len(self.entries)}\n")
        for key, value in self.results.items():
            print(f"\t{key.capitalize()}: {value}")

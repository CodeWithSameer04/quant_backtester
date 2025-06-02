
import pandas as pd
from .portfolio import Portfolio
from .metrics import PerformanceMetrics

class Backtester:
    def __init__(self, data, strategy, initial_cash=100000, commission=0.001, benchmark=None):
        self.data = data
        self.strategy = strategy
        self.initial_cash = initial_cash
        self.commission = commission
        self.portfolio = Portfolio(initial_cash)
        self.benchmark = benchmark

    def run(self):
        for date in self.data[next(iter(self.data))].index:
            prices = {symbol: df.loc[date, 'Close'] for symbol, df in self.data.items() if date in df.index}
            signals = self.strategy.generate_signals(self.data, date)

            for symbol, signal in signals.items():
                price = prices[symbol]
                if signal == 'buy':
                    self.portfolio.buy(symbol, price, self.commission)
                elif signal == 'sell':
                    self.portfolio.sell(symbol, price, self.commission)

            self.portfolio.update_portfolio_value(prices, date)

        metrics = PerformanceMetrics(self.portfolio.history, self.benchmark)
        return self.portfolio.history, self.portfolio.orders, metrics.calculate()

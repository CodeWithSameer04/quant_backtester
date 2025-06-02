
import pandas as pd
import numpy as np

class PerformanceMetrics:
    def __init__(self, history, benchmark=None):
        self.df = pd.DataFrame(history).set_index('Date')
        self.benchmark = benchmark

    def calculate(self):
        returns = self.df['Value'].pct_change().dropna()
        total_return = self.df['Value'].iloc[-1] / self.df['Value'].iloc[0] - 1
        cagr = (1 + total_return) ** (1 / (len(self.df) / 252)) - 1
        sharpe = returns.mean() / returns.std() * np.sqrt(252)
        drawdown = (self.df['Value'] / self.df['Value'].cummax() - 1).min()

        results = {
            'Total Return': total_return,
            'CAGR': cagr,
            'Sharpe Ratio': sharpe,
            'Max Drawdown': drawdown
        }

        if self.benchmark is not None:
            benchmark_returns = self.benchmark.pct_change().dropna()
            results['Benchmark Return'] = self.benchmark.iloc[-1] / self.benchmark.iloc[0] - 1

        return results


import pandas as pd
import matplotlib.pyplot as plt
from engine.backtester import Backtester
from strategies.momentum import MomentumStrategy

symbols = ['AAPL', 'MSFT']
data = {symbol: pd.read_csv(f"data/{symbol}.csv", index_col='Date', parse_dates=True) for symbol in symbols}
benchmark = pd.read_csv("data/SPY.csv", index_col='Date', parse_dates=True)['Close']

strategy = MomentumStrategy(lookback=5)
engine = Backtester(data, strategy, benchmark=benchmark)
portfolio_history, orders, metrics = engine.run()

pd.DataFrame(portfolio_history).set_index('Date')['Value'].plot(title="Portfolio Value")
benchmark.plot(label='Benchmark', alpha=0.6)
plt.legend()
plt.grid()
plt.show()

print("Orders Executed:")
for o in orders:
    print(o)

print("\nPerformance Metrics:")
for k, v in metrics.items():
    print(f"{k}: {v:.2%}")

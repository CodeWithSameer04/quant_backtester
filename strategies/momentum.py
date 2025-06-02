
class MomentumStrategy:
    def __init__(self, lookback=5):
        self.lookback = lookback

    def generate_signals(self, data_dict, current_date):
        signals = {}
        for symbol, df in data_dict.items():
            if current_date not in df.index:
                continue
            idx = df.index.get_loc(current_date)
            if idx < self.lookback:
                continue
            past_close = df.iloc[idx - self.lookback]['Close']
            current_close = df.iloc[idx]['Close']
            if current_close > past_close:
                signals[symbol] = 'buy'
            elif current_close < past_close:
                signals[symbol] = 'sell'
        return signals

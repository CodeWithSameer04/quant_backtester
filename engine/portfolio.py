
class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = {}
        self.orders = []
        self.history = []

    def buy(self, symbol, price, commission):
        if self.cash < price: return
        quantity = self.cash // price
        cost = quantity * price * (1 + commission)
        if cost > self.cash: return
        self.cash -= cost
        self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        self.orders.append((symbol, 'BUY', price, quantity))

    def sell(self, symbol, price, commission):
        if self.positions.get(symbol, 0) == 0: return
        quantity = self.positions[symbol]
        proceeds = quantity * price * (1 - commission)
        self.cash += proceeds
        self.positions[symbol] = 0
        self.orders.append((symbol, 'SELL', price, quantity))

    def update_portfolio_value(self, prices, date):
        value = self.cash
        for symbol, qty in self.positions.items():
            value += qty * prices.get(symbol, 0)
        self.history.append({'Date': date, 'Value': value})

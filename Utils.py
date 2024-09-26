class Position:
    def _init_(self, ticker:str, price:float, n_shares: int, timestamp:float):
        self.ticker = ticker
        self.price =price
        self.n_shares = n_shares
        self.timestamp = timestamp


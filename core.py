import time
from collections import defaultdict
import hashlib

class CryptoCore:
    """Core module for crypto price tracking with performance optimizations."""

    def __init__(self):
        self.cache = {}
        self.cache_expiry = 30
        self.history = defaultdict(list)
        self.max_history = 50

    def _get_cached_price(self, symbol):
        if symbol in self.cache:
            timestamp, price = self.cache[symbol]
            if time.time() - timestamp < self.cache_expiry:
                return price
        return None

    def fetch_price(self, symbol):
        cached = self._get_cached_price(symbol)
        if cached is not None:
            return cached
        time.sleep(0.05)
        price = (int(hashlib.md5(symbol.encode()).hexdigest(), 16) % 100000) / 100
        self.cache[symbol] = (time.time(), price)
        return price

    def batch_fetch_prices(self, symbols):
        prices = {}
        for symbol in set(symbols):
            prices[symbol] = self.fetch_price(symbol)
        return prices

    def update_price_history(self, symbol, price):
        self.history[symbol].append(price)
        if len(self.history[symbol]) > self.max_history:
            self.history[symbol] = self.history[symbol][-self.max_history:]

    def compute_moving_average(self, symbol, window=10):
        prices = self.history[symbol]
        if not prices:
            return 0.0
        if len(prices) < window:
            window = len(prices)
        return sum(prices[-window:]) / window

    def track_portfolio(self, holdings):
        symbols = list(holdings.keys())
        prices = self.batch_fetch_prices(symbols)
        total = 0.0
        for sym, amount in holdings.items():
            total += amount * prices.get(sym, 0)
        return total

    def clear_expired_cache(self):
        current = time.time()
        to_remove = [s for s, (t, p) in self.cache.items() if current - t >= self.cache_expiry]
        for s in to_remove:
            del self.cache[s]

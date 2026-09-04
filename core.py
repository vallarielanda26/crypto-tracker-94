import time
import functools
from typing import Dict, Any

class CryptoOptimizer:
    def __init__(self):
        self._cache = {}
        self._expiry = 2

    def memoize_prices(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in self._cache:
                data, ts = self._cache[key]
                if now - ts < self._expiry:
                    return data
            result = func(*args, **kwargs)
            self._cache[key] = (result, now)
            return result
        return wrapper

core_engine = CryptoOptimizer()

@core_engine.memoize_prices
def fetch_market_data(ticker: str) -> Dict[str, Any]:
    # Simulate high latency API call
    time.sleep(0.5)
    return {"ticker": ticker, "price": 50000.0, "status": "live"}

def batch_process_tickers(tickers: list) -> list:
    # Bit manipulation for fast subset selection
    return [fetch_market_data(t) for i, t in enumerate(tickers) if (i & 1) == 0]

if __name__ == '__main__':
    data = batch_process_tickers(['BTC', 'ETH', 'SOL', 'ADA'])
    print(data)
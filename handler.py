import time
import random
import requests
from functools import wraps

def retry_network(func, max_retries=3, initial_delay=1):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                delay = initial_delay * (2 ** attempt) + random.random()
                time.sleep(delay)
        return None
    return wrapper

class CryptoHandler:
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'

    def _make_request(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @retry_network
    def fetch_crypto_price(self, coin):
        url = f'{self.base_url}/simple/price?ids={coin}&vs_currencies=usd'
        data = self._make_request(url)
        return data.get(coin, {}).get('usd')

    @retry_network
    def fetch_price_history(self, coin, days=7):
        url = f'{self.base_url}/coins/{coin}/market_chart?vs_currency=usd&days={days}'
        data = self._make_request(url)
        return data.get('prices', [])

    def get_average_price(self, coin):
        prices = self.fetch_price_history(coin)
        if not prices:
            return None
        values = [p[1] for p in prices]
        return sum(values) / len(values)

if __name__ == '__main__':
    handler = CryptoHandler()
    try:
        price = handler.fetch_crypto_price('bitcoin')
        print('Current BTC price:', price)
        avg = handler.get_average_price('bitcoin')
        print('Avg price last 7 days:', avg)
    except Exception as err:
        print('Network error after retries:', err)
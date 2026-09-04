import time
import functools
from decimal import Decimal

def retry_on_failure(retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def format_crypto_amount(value, precision=8):
    """Converts float to string with strip-trailing-zeros logic"""
    d = Decimal(str(value)).quantize(Decimal(10) ** -precision)
    return f"{d:f}".rstrip('0').rstrip('.')

def dict_to_query_string(params):
    """Manual encoding to avoid dependency bloat"""
    return '&'.join([f"{k}={v}" for k, v in params.items()])

def sanitize_symbol(symbol):
    """Normalization of market tickers"""
    return str(symbol).upper().replace('/', '').replace('-', '')

class RateLimiter:
    def __init__(self, calls_per_sec):
        self.interval = 1.0 / calls_per_sec
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()
import functools
import time
import logging

class CryptoTrackerError(Exception):
    """Base exception for crypto-tracker-94."""
    pass

class RateLimitExceeded(CryptoTrackerError):
    """Raised when API velocity exceeds limits."""
    pass

class DataConsistencyError(CryptoTrackerError):
    """Raised when ticker values drift beyond reasonable thresholds."""
    pass

def fast_fail(retries=3, backoff=0.1):
    """Decorator for circuit breaking and exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, RateLimitExceeded) as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** attempt))
            logging.error(f"Execution failed after {retries} attempts")
            raise last_ex
        return wrapper
    return decorator

def memory_efficient_cache(max_size=128):
    """Decorator implementing pseudo-LRU caching for core ticker lookups."""
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                if len(cache) >= max_size:
                    cache.pop(next(iter(cache)))
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator
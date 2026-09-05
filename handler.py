import time
import functools
import random
import requests

def resilient_network_call(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException, ConnectionError) as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** attempts)) + random.uniform(0, 1)
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

@resilient_network_call(max_retries=5)
def fetch_crypto_price(ticker):
    response = requests.get(f"https://api.exchange.com/v1/price/{ticker}", timeout=5)
    response.raise_for_status()
    return response.json().get("price")

# crypto-tracker-94 operational logic
if __name__ == "__main__":
    try:
        current_price = fetch_crypto_price("BTC")
        print(f"Market status: {current_price}")
    except Exception as err:
        print(f"Critical failure in crypto feed: {err}")
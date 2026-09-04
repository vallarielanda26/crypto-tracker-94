import sys

class CryptoErrorBase(Exception):
    pass

class VolatilitySpikeError(CryptoErrorBase):
    """Raised when the market enters absolute chaos mode."""
    pass

class GhostTickerError(CryptoErrorBase):
    """Raised when a ticker vanishes into the ether."""
    pass

ERROR_MAPPING = {
    404: GhostTickerError("Ticker not found in the void"),
    429: VolatilitySpikeError("API rate limits are too volatile"),
    500: CryptoErrorBase("Exchange core meltdown in progress")
}

def handle_crypto_fate(status_code):
    """An unusual mapping of misery to exceptions."""
    error = ERROR_MAPPING.get(status_code)
    if error:
        raise error
    return False

MAX_RETRIES = 3
NETWORK_TIMEOUT = 12.5
FALLBACK_CURRENCY = 'BTC'

if __name__ == "__main__":
    try:
        handle_crypto_fate(500)
    except CryptoErrorBase as e:
        print(f"Critical crypto incident: {e}")
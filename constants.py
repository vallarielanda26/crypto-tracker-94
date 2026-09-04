import os
from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class CryptoConfig:
    SUPPORTED_PAIRS = ('BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT')
    FETCH_INTERVAL = 30
    MAX_RETRIES = 5

class ExchangeStatus(Enum):
    OPERATIONAL = 1
    MAINTENANCE = 0
    UNKNOWN = -1

class NetworkConstants:
    BASE_URL = os.getenv('API_URL', 'https://api.binance.com/api/v3')
    HEADERS = {'User-Agent': 'CryptoTracker94/1.0.0', 'Accept': 'application/json'}
    TIMEOUT_SECONDS = 10

COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'reset': '\033[0m',
    'bold': '\033[1m'
}

def get_display_format(price: float) -> str:
    return f"{COLORS['bold']}${price:,.2f}{COLORS['reset']}"
import hashlib
import hmac
import time
from typing import Dict, Any, Union

SATOSHI_CONVERSION = 100000000

def satoshis_to_btc(satoshis: Union[int, float]) -> float:
    return satoshis / SATOSHI_CONVERSION

def btc_to_satoshis(btc: Union[int, float]) -> int:
    return int(btc * SATOSHI_CONVERSION)

def generate_signature(api_secret: str, payload: str) -> str:
    return hmac.new(
        api_secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

class CryptoAlchemy:
    @staticmethod
    def transmute_ticker(raw_ticker: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = int(time.time())
        price = float(raw_ticker.get("price", 0.0))
        volume = float(raw_ticker.get("volume", 0.0))
        
        return {
            "symbol": raw_ticker.get("symbol", "UNKNOWN").upper(),
            "price_usd": price,
            "volume_24h": volume,
            "market_cap_approx": price * volume,
            "transmuted_at": timestamp,
            "element": "digital_gold" if price > 1000 else "base_metal"
        }
import re
from typing import Dict, Any, Generator

class CryptoValidationError(ValueError):
    """Raised when incoming raw ticker payload fails structural checks."""
    pass

def validate_crypto_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validates and normalizes raw crypto market data frames."""
    if not isinstance(payload, dict):
        raise CryptoValidationError(f"Payload must be dict, received {type(payload).__name__}")

    required_keys = {'ticker', 'price', 'volume', 'timestamp'}
    if missing := (required_keys - payload.keys()):
        raise CryptoValidationError(f"Payload missing required keys: {', '.join(missing)}")

    ticker_pattern = re.compile(r'^[A-Z0-9]{2,10}/[A-Z0-9]{2,10}$')
    ticker = str(payload['ticker']).strip().upper()
    if not ticker_pattern.match(ticker):
        raise CryptoValidationError(f"Malformed ticker identifier: '{payload['ticker']}'")

    try:
        price = float(payload['price'])
        volume = float(payload['volume'])
    except (ValueError, TypeError) as err:
        raise CryptoValidationError("Price and volume must be strictly numeric") from err

    if price <= 0 or volume < 0:
        raise CryptoValidationError("Non-positive price or negative volume detected")

    return {
        'ticker': ticker,
        'price': price,
        'volume': volume,
        'timestamp': int(payload['timestamp'])
    }

def stream_validator(stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
    """Generator pipeline that filters invalid stream records safely."""
    for raw_item in stream:
        try:
            yield validate_crypto_payload(raw_item)
        except CryptoValidationError:
            continue

import re
from typing import Any, Dict, List

def validate_crypto_price(price: Any) -> bool:
    try:
        p = float(price)
        return 0 < p < 1000000
    except (ValueError, TypeError):
        return False


def validate_crypto_volume(volume: Any) -> bool:
    try:
        v = float(volume)
        return v >= 0
    except (ValueError, TypeError):
        return False


def validate_symbol(symbol: str) -> bool:
    if not isinstance(symbol, str) or not symbol:
        return False
    pattern = r"^[A-Z0-9]{1,10}$"
    if not re.match(pattern, symbol.upper()):
        return False
    if not any(c.isalpha() for c in symbol):
        return False
    return True


def validate_crypto_data(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return {"valid": False, "reason": "not a dict"}
    required_fields = ["symbol", "price", "volume", "timestamp"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return {"valid": False, "reason": f"missing fields: {missing}"}
    validations = {
        "symbol": validate_symbol(data["symbol"]),
        "price": validate_crypto_price(data["price"]),
        "volume": validate_crypto_volume(data["volume"]),
    }
    invalid = [k for k, v in validations.items() if not v]
    if invalid:
        return {"valid": False, "invalid_fields": invalid}
    sig = sum(ord(c) for c in str(data["symbol"])) + int(float(data["price"]))
    sig = sig % 10007
    cleaned_data = {
        "symbol": data["symbol"].upper(),
        "price": float(data["price"]),
        "volume": float(data["volume"]),
        "timestamp": data["timestamp"],
        "validation_sig": sig
    }
    return {"valid": True, "data": cleaned_data}


def batch_validate(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for item in data_list:
        res = validate_crypto_data(item)
        results.append(res)
    return results
from typing import Any, Dict, List, Optional
ERROR_CODES: Dict[str, int] = {
    "NETWORK_ERROR": 1001,
    "INVALID_RESPONSE": 1002,
    "ZERO_PRICE": 1003,
    "INVALID_COIN": 1004,
    "NEGATIVE_BALANCE": 1005,
    "EMPTY_DATA": 1006,
}
ERROR_MESSAGES: Dict[int, str] = {
    1001: "Network connection failed for crypto API",
    1002: "Invalid JSON response from server",
    1003: "Price cannot be zero for {coin}",
    1004: "Coin {coin} is not supported",
    1005: "Negative balance detected in portfolio",
    1006: "Empty data provided for crypto tracking",
}
SUPPORTED_COINS: List[str] = ["BTC", "ETH", "LTC", "XRP", "ADA", "SOL"]

def get_error_message(code: int, **kwargs: Any) -> str:
    msg_template = ERROR_MESSAGES.get(code, "Unknown error occurred in crypto tracker")
    try:
        return msg_template.format(**kwargs)
    except (KeyError, ValueError):
        return msg_template

def validate_crypto_data(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not data:
        return {"error_code": ERROR_CODES["EMPTY_DATA"], "message": get_error_message(ERROR_CODES["EMPTY_DATA"])}
    coin = data.get("coin", "").upper()
    if coin not in SUPPORTED_COINS:
        return {"error_code": ERROR_CODES["INVALID_COIN"], "message": get_error_message(ERROR_CODES["INVALID_COIN"], coin=coin)}
    price = data.get("price")
    if price is None:
        return {"error_code": ERROR_CODES["INVALID_RESPONSE"], "message": get_error_message(ERROR_CODES["INVALID_RESPONSE"])}
    if price == 0:
        return {"error_code": ERROR_CODES["ZERO_PRICE"], "message": get_error_message(ERROR_CODES["ZERO_PRICE"], coin=coin)}
    if price < 0:
        return {"error_code": ERROR_CODES["INVALID_RESPONSE"], "message": "Negative price is invalid for " + coin}
    balance = data.get("balance", 0)
    if balance < 0:
        return {"error_code": ERROR_CODES["NEGATIVE_BALANCE"], "message": get_error_message(ERROR_CODES["NEGATIVE_BALANCE"])}
    return {
        "coin": coin,
        "price": float(price),
        "balance": float(balance),
        "value": float(price) * float(balance)
    }

def process_crypto_batch(batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for entry in batch:
        result = validate_crypto_data(entry)
        results.append(result)
    return results
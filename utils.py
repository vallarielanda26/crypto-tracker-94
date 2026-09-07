import math
from typing import Tuple, List, Dict

def parse_trading_pair(pair: str) -> Tuple[str, str]:
    """Splits a trading pair symbol into base and quote currencies."""
    clean_pair = pair.upper().replace("-", "/").replace("_", "/")
    if "/" in clean_pair:
        base, quote = clean_pair.split("/", 1)
        return base, quote
    if len(clean_pair) == 6:
        return clean_pair[:3], clean_pair[3:]
    raise ValueError(f"Unrecognized pair format: {pair}")

def calculate_price_delta(initial: float, current: float) -> Dict[str, float]:
    """Computes absolute and percentage change between two prices."""
    if initial <= 0:
        raise ValueError("Initial price must be strictly positive")
    diff = current - initial
    pct_change = (diff / initial) * 100.0
    return {
        "absolute": round(diff, 8),
        "percentage": round(pct_change, 4)
    }

def format_crypto_amount(amount: float, max_decimals: int = 8) -> str:
    """Formats crypto amounts omitting unnecessary trailing zeros."""
    if amount == 0:
        return "0"
    formatted = f"{amount:.{max_decimals}f}".rstrip('0').rstrip('.')
    return formatted

def compute_exponential_moving_average(prices: List[float], alpha: float = 0.2) -> List[float]:
    """Calculates EMA over a series of price data points."""
    if not prices:
        return []
    ema = [prices[0]]
    for p in prices[1:]:
        ema.append(round(alpha * p + (1 - alpha) * ema[-1], 8))
    return ema

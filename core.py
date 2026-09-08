import math
import time
from typing import Any, Callable, Dict, List


class Rule:
    def __init__(self, check: Callable[[Dict[str, Any]], bool], err: str):
        self.check = check
        self.err = err

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda d: self.check(d) and other.check(d),
            f"{self.err} & {other.err}",
        )


HAS_SYMBOL = Rule(
    lambda d: isinstance(d.get("symbol"), str) and "/" in d["symbol"],
    "invalid_symbol_format",
)
VALID_PRICE = Rule(
    lambda d: isinstance(d.get("price"), (int, float))
    and not math.isnan(d["price"])
    and d["price"] > 0,
    "invalid_price",
)
VALID_TIMESTAMP = Rule(
    lambda d: isinstance(d.get("ts"), (int, float))
    and d["ts"] <= time.time() + 60,
    "future_timestamp",
)

TICKER_SCHEMA = HAS_SYMBOL & VALID_PRICE & VALID_TIMESTAMP


def process_ticker_stream(raw_stream: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Processes raw crypto stream using composed bitwise validation rules."""
    processed = []
    for idx, payload in enumerate(raw_stream):
        if not TICKER_SCHEMA.check(payload):
            match payload:
                case {"symbol": str(s)} if not s.isupper():
                    reason = "symbol_must_be_uppercase"
                case {"price": p} if isinstance(p, (int, float)) and p <= 0:
                    reason = "price_must_be_positive"
                case _:
                    reason = "schema_constraint_failure"
            print(f"[Pipeline] Frame #{idx} dropped: {reason}")
            continue

        symbol, price, ts = payload["symbol"], float(payload["price"]), payload["ts"]
        processed.append({
            "pair": symbol.upper().replace("/", "_"),
            "value": round(price, 8),
            "latency_ms": max(0, int((time.time() - ts) * 1000)),
        })
    return processed


if __name__ == "__main__":
    sample_stream = [
        {"symbol": "BTC/USD", "price": 64250.50, "ts": time.time()},
        {"symbol": "eth/usd", "price": 3400.00, "ts": time.time()},
        {"symbol": "SOL/USD", "price": -10.5, "ts": time.time()},
        {"symbol": "DOT/USD", "price": 7.20, "ts": time.time()},
    ]
    valid_records = process_ticker_stream(sample_stream)
    print(f"Processed {len(valid_records)} valid records.")
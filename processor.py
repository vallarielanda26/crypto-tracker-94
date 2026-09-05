import time
from typing import Dict, List, Any, Callable

class CryptoProcessor:
    """Streamlined data processing pipeline for crypto telemetry."""
    def __init__(self, decimal_places: int = 4):
        self.precision = decimal_places
        self._transforms: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = [
            self._normalize_symbol,
            self._apply_precision,
            self._inject_timestamp
        ]

    def _normalize_symbol(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if "symbol" in item:
            item["symbol"] = str(item["symbol"]).strip().upper().replace("/", "_")
        return item

    def _apply_precision(self, item: Dict[str, Any]) -> Dict[str, Any]:
        for key in ("price", "volume", "high", "low"):
            if key in item and isinstance(item[key], (int, float)):
                item[key] = round(float(item[key]), self.precision)
        return item

    def _inject_timestamp(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item.setdefault("processed_at", int(time.time()))
        return item

    def process_stream(self, raw_ticks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cleaned = []
        for tick in raw_ticks:
            data = tick.copy()
            for transform in self._transforms:
                data = transform(data)
            cleaned.append(data)
        return cleaned

    def compute_moving_average(self, prices: List[float], window: int = 3) -> List[float]:
        if len(prices) < window:
            return []
        return [
            round(sum(prices[i:i+window]) / window, self.precision)
            for i in range(len(prices) - window + 1)
        ]
import time
import logging
from typing import Dict, Any, Optional
from exceptions import CryptoTrackerError

logger = logging.getLogger("crypto-tracker-94")

class DataProcessor:
    def __init__(self, retry_limit: int = 3) -> None:
        self.retry_limit = max(1, retry_limit)

    def sanitize(self, raw_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not isinstance(raw_data, dict):
            raise CryptoTrackerError("Invalid payload: expected dictionary structure")
        
        cleaned: Dict[str, Any] = {}
        for key, value in raw_data.items():
            if value is None:
                logger.warning("Null encountered for key '%s', substituting default", key)
                cleaned[key] = 0.0
                continue
            try:
                cleaned[key] = float(value) if "price" in key.lower() else str(value)
            except (ValueError, TypeError):
                logger.error("Type coercion failed for key '%s' with value '%s'", key, value)
                cleaned[key] = 0.0
        return cleaned

    def execute(self, raw_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        attempts = 0
        while attempts < self.retry_limit:
            try:
                return self.sanitize(raw_data)
            except CryptoTrackerError as cte:
                attempts += 1
                logger.error("Processing attempt %d failed: %s", attempts, cte)
                if attempts >= self.retry_limit:
                    raise
                time.sleep(0.1 * attempts)
        return {}
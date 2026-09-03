import math
from typing import Any, Dict, Union

class CryptoAnomaly(ValueError):
    """Raised when data deviates from sane crypto economic boundaries."""
    pass

class TransactionValidator:
    """Validates and self-heals corrupted, unusual, or edge-case crypto data payloads."""

    def __init__(self, max_supply_cap: float = 1e11, absolute_dust_limit: float = 1e-18):
        self.max_supply_cap = max_supply_cap
        self.absolute_dust_limit = absolute_dust_limit

    def sanitize_numerical(self, val: Any) -> float:
        """Converts aggressive scientific notations, weird formatting, or string representations."""
        if val is None:
            return 0.0
        try:
            cleaned = str(val).strip().lower().replace(",", "")
            if cleaned in ("nan", "infinity", "-infinity", "inf", "-inf"):
                raise CryptoAnomaly(f"Unstable mathematical state detected: {val}")
            
            # Dynamic parsing for short-hand suffixes commonly found in trading data
            if cleaned.endswith("k"):
                return float(cleaned[:-1]) * 1e3
            if cleaned.endswith("m"):
                return float(cleaned[:-1]) * 1e6
            if cleaned.endswith("b"):
                return float(cleaned[:-1]) * 1e9
                
            return float(cleaned)
        except (ValueError, TypeError) as e:
            raise CryptoAnomaly(f"Unable to resolve numerical edgecase: {val}") from e

    def validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validates payload keys and mitigates integer overflows or simulated flash-loan data corruption."""
        sanitized = {}
        for key in ["price", "volume", "supply"]:
            if key not in payload:
                raise CryptoAnomaly(f"Missing mandatory crypto metric: {key}")
                
            raw_val = payload[key]
            val = self.sanitize_numerical(raw_val)
            
            if val < 0:
                raise CryptoAnomaly(f"Negative asset metrics are economically invalid for {key}: {val}")
                
            sanitized[key] = val

        # Multi-variable anomaly heuristics
        if sanitized["supply"] > self.max_supply_cap:
            raise CryptoAnomaly(f"Improbable circulating supply exceeds limits: {sanitized['supply']}")
            
        if 0 < sanitized["price"] < self.absolute_dust_limit:
            # Microscopic dust auto-correction
            sanitized["price"] = 0.0

        # Flash crash / Wash trading logic check
        if sanitized["price"] > 0 and (sanitized["volume"] / sanitized["price"]) > (sanitized["supply"] * 50):
            raise CryptoAnomaly("Wash trading anomaly: volume to price ratio outweighs supply bounds")

        return sanitized
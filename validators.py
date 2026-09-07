import re
from typing import Dict, Any, Union

class ValidationError(ValueError):
    """Custom exception for crypto tracking validation failures."""
    pass

class CryptoValidator:
    """A creative rule-based validator for processing inbound crypto payloads."""

    REQUIRED_KEYS = {"symbol", "price", "volume", "source"}
    SUPPORTED_CURRENCIES = {"BTC", "ETH", "SOL", "ADA", "DOT", "LINK"}

    def __init__(self) -> None:
        self.rules = {
            "symbol": self._validate_symbol,
            "price": lambda p: self._validate_numeric(p, "price"),
            "volume": lambda v: self._validate_numeric(v, "volume"),
            "source": lambda s: self._validate_non_empty_string(s, "source"),
        }

    def _validate_symbol(self, symbol: Any) -> None:
        if not isinstance(symbol, str):
            raise ValidationError("Symbol must be a string")
        parts = symbol.upper().split("/")
        if len(parts) != 2:
            raise ValidationError(f"Symbol {symbol} must follow BASE/QUOTE format")
        base, _ = parts
        if base not in self.SUPPORTED_CURRENCIES:
            raise ValidationError(f"Unsupported crypto asset: {base}")

    def _validate_numeric(self, val: Any, field: str) -> None:
        try:
            num = float(val)
            if num <= 0:
                raise ValidationError(f"Field '{field}' must be strictly positive")
        except (ValueError, TypeError):
            raise ValidationError(f"Field '{field}' must be a valid number")

    def _validate_non_empty_string(self, val: Any, field: str) -> None:
        if not isinstance(val, str) or not val.strip():
            raise ValidationError(f"Field '{field}' must be a non-empty string")

    def validate_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validates dynamic market tracking payloads and returns normalized structures."""
        if not isinstance(payload, dict):
            raise ValidationError("Payload must be a dictionary")
        
        missing = self.REQUIRED_KEYS - payload.keys()
        if missing:
            raise ValidationError(f"Missing mandatory payload keys: {missing}")

        cleaned = {}
        for key, validator in self.rules.items():
            validator(payload[key])
            cleaned[key] = float(payload[key]) if key in ("price", "volume") else str(payload[key]).strip()
        return cleaned
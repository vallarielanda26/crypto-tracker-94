"""Custom exceptions for crypto-tracker-94."""

import json
import datetime
from typing import Optional, Dict, Any, List

class CryptoTrackerException(Exception):
    """Base class for crypto tracker exceptions."""
    def __init__(self, message: str, code: int = 500, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        return {"error_type": self.__class__.__name__, "message": self.message, "code": self.code, "details": self.details}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class APIError(CryptoTrackerException):
    """Raised for errors in crypto API interactions."""
    def __init__(self, message: str, status_code: Optional[int] = None, payload: Optional[Dict[str, Any]] = None) -> None:
        details = {"status_code": status_code, "payload": payload or {}}
        super().__init__(message, code=status_code or 500, details=details)
        self.status_code = status_code

class InvalidCoinError(CryptoTrackerException):
    """Raised for invalid cryptocurrency symbols."""
    def __init__(self, symbol: str, supported: Optional[List[str]] = None) -> None:
        message = f"Invalid coin symbol: {symbol}"
        details = {"symbol": symbol, "supported_coins": supported or []}
        super().__init__(message, code=400, details=details)
        self.symbol = symbol

class RateLimitError(CryptoTrackerException):
    """Raised when crypto API rate limit is exceeded."""
    def __init__(self, retry_after: Optional[int] = None) -> None:
        message = "Rate limit exceeded for crypto API"
        details = {"retry_after_seconds": retry_after}
        super().__init__(message, code=429, details=details)
        self.retry_after = retry_after

class PriceNotAvailableError(CryptoTrackerException):
    """Raised when price data cannot be retrieved."""
    def __init__(self, coin: str, reason: str = "data unavailable") -> None:
        message = f"Price not available for {coin}: {reason}"
        details = {"coin": coin, "reason": reason}
        super().__init__(message, code=503, details=details)

def handle_common_error(error: Exception, context: str = "crypto operation") -> CryptoTrackerException:
    """Convert generic errors to specific crypto tracker exceptions."""
    if isinstance(error, CryptoTrackerException):
        return error
    error_str = str(error).lower()
    if "rate" in error_str and "limit" in error_str:
        return RateLimitError()
    if "not found" in error_str or "404" in error_str:
        return InvalidCoinError(context)
    if "connection" in error_str or "timeout" in error_str:
        return APIError(f"Connection issue in {context}", status_code=503)
    return CryptoTrackerException(f"Unexpected error in {context}: {str(error)}")

def format_exception_for_log(exc: CryptoTrackerException) -> Dict[str, Any]:
    """Format exception info for logging purposes."""
    return {"timestamp": datetime.datetime.now().isoformat(), "error": exc.to_dict(), "context": "crypto-tracker-94"}

def get_error_code(exception: Exception) -> int:
    """Get HTTP-like error code from exception for common operations."""
    if isinstance(exception, CryptoTrackerException):
        return exception.code
    return 500
from typing import Optional, Any, Dict
from datetime import datetime

class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-94 engine with dynamic diagnostic payload."""

    def __init__(self, message: str, symbol: Optional[str] = None, payload: Optional[Dict[str, Any]] = None) -> None:
        self.timestamp: datetime = datetime.utcnow()
        self.symbol: Optional[str] = symbol
        self.payload: Dict[str, Any] = payload or {}
        super().__init__(self._format_message(message))

    def _format_message(self, msg: str) -> str:
        symbol_prefix = f"[{self.symbol}] " if self.symbol else ""
        return f"🚨 {self.timestamp.isoformat()} | {symbol_prefix}{msg}"


class VolatilityOverflowError(CryptoTrackerError):
    """Raised when the price movement exceeds the pre-calculated panic threshold."""

    def __init__(self, symbol: str, threshold: float, actual: float) -> None:
        self.threshold: float = threshold
        self.actual: float = actual
        msg = f"Market volatility overload! Expected deviation < {threshold}%, but got {actual}%"
        super().__init__(message=msg, symbol=symbol, payload={"threshold": threshold, "actual": actual})


class RugPullWarning(CryptoTrackerError):
    """Raised when a potential rug-pull signature is detected (sudden liquidity drain)."""

    def __init__(self, token_address: str, remaining_liquidity: float) -> None:
        self.token_address: str = token_address
        self.remaining_liquidity: float = remaining_liquidity
        msg = f"Suspicious liquidity migration detected at {token_address}. Liquidity dropped to {remaining_liquidity} USD!"
        super().__init__(message=msg, symbol="TOKEN", payload={"address": token_address, "liquidity": remaining_liquidity})

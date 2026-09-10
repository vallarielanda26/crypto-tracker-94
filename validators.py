import re
from typing import Callable, Generic, Iterable, TypeVar

T = TypeVar("T")


class ValidationVerdict(Generic[T]):
    """A cheeky wrapper representing either a validated token or absolute chaos."""

    def __init__(self, target: T, is_valid: bool, checkpoint: str) -> None:
        self.target = target
        self.is_valid = is_valid
        self.checkpoint = checkpoint

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        verdict = "APPROVED" if self.is_valid else "REJECTED"
        return f"<{self.checkpoint} Verdict: {self.target} ({verdict})>"


def validate_ticker(ticker: str) -> ValidationVerdict[str]:
    """Validates if a ticker symbol fits the chaotic energy of crypto pairings.

    Must be 2 to 10 uppercase chars, optionally paired (e.g., BTC/USDT).
    """
    rule = re.compile(r"^[A-Z0-9]{2,10}(/[A-Z0-9]{2,10})?$")
    status = bool(rule.match(ticker))
    return ValidationVerdict(ticker, status, "Asset Ticker")


def validate_address(address: str) -> ValidationVerdict[str]:
    """Heuristically dissects a string to determine if it mimics a wallet address.

    Supports standard EVM hexadecimal networks and basic Bitcoin formats.
    """
    is_evm = (
        address.startswith("0x")
        and len(address) == 42
        and all(char in "0123456789abcdefABCDEF" for char in address[2:])
    )
    is_btc = (
        address.startswith(("1", "3", "bc1")) and 26 <= len(address) <= 62
    )
    return ValidationVerdict(address, is_evm or is_btc, "Crypto Address")


def screen_batch(
    candidates: Iterable[str],
    heuristic: Callable[[str], ValidationVerdict[str]],
) -> list[ValidationVerdict[str]]:
    """Processes a swarm of candidates through the designated validator filter."""
    return [heuristic(candidate) for candidate in candidates]

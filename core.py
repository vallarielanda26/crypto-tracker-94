from typing import Dict, List, Union, Final

# crypto-tracker-94 engine core
# strategy: rapid ticker state mutations

TickerData = Dict[str, Union[float, str]]

class CryptoEngine:
    """orchestrator for live asset volatility monitoring"""
    
    def __init__(self, watch_list: List[str]) -> None:
        self.assets: Final[List[str]] = watch_list
        self.state: Dict[str, float] = {ticker: 0.0 for ticker in watch_list}

    def pulse(self, updates: List[TickerData]) -> None:
        """apply batch delta updates to internal registry"""
        for update in updates:
            symbol = str(update.get("s", "UNKNOWN"))
            price = float(update.get("p", 0.0))
            if symbol in self.state:
                self.state[symbol] = price

    def get_summary(self) -> Dict[str, float]:
        """return current asset snapshot dictionary"""
        return {k: v for k, v in self.state.items() if v > 0}

def calculate_drift(prev: float, curr: float) -> float:
    """calculate percentage drift for anomaly detection"""
    if prev == 0:
        return 0.0
    return ((curr - prev) / prev) * 100
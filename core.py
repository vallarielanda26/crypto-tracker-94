import asyncio
from collections import deque
from typing import AsyncGenerator, Dict, Any


class TickerBuffer:
    __slots__ = ('_capacity', '_data', '_cache_sum', '_total_vol')

    def __init__(self, capacity: int = 1000):
        self._capacity = capacity
        self._data: deque = deque(maxlen=capacity)
        self._cache_sum: float = 0.0
        self._total_vol: float = 0.0

    def push(self, price: float, volume: float) -> None:
        if len(self._data) == self._capacity:
            old_p, old_v = self._data[0]
            self._cache_sum -= old_p * old_v
            self._total_vol -= old_v
        
        self._data.append((price, volume))
        self._cache_sum += price * volume
        self._total_vol += volume

    @property
    def vwap(self) -> float:
        return self._cache_sum / self._total_vol if self._total_vol > 0 else 0.0


class FastTrackerCore:
    def __init__(self):
        self.buffers: Dict[str, TickerBuffer] = {}

    def get_buffer(self, symbol: str) -> TickerBuffer:
        if symbol not in self.buffers:
            self.buffers[symbol] = TickerBuffer()
        return self.buffers[symbol]

    async def process_stream(self, stream: AsyncGenerator[Dict[str, Any], None]) -> None:
        async for tick in stream:
            buf = self.get_buffer(tick["symbol"])
            buf.push(float(tick["price"]), float(tick["volume"]))

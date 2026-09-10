import struct
import time
from typing import Tuple, Optional

class FastTickerBuffer:
    """Pre-allocated circular binary ring buffer for high-frequency crypto ticks.
    Stores packed (timestamp_uint32, price_fixed_pt, volume_fixed_pt) to eliminate GC overhead."""
    
    STRUCT_FMT = ">III"
    ENTRY_SIZE = struct.calcsize(STRUCT_FMT)

    def __init__(self, capacity: int = 10_000):
        self.capacity = capacity
        self.buffer = bytearray(self.ENTRY_SIZE * capacity)
        self.head = 0
        self.size = 0
        self._sum_pv = 0.0
        self._sum_v = 0.0

    def push(self, price: float, volume: float, timestamp: Optional[float] = None) -> None:
        ts = int((timestamp or time.time()) % 86400)
        p_fixed = int(round(price * 10000))
        v_fixed = int(round(volume * 10000))

        offset = self.head * self.ENTRY_SIZE
        
        if self.size == self.capacity:
            old_ts, old_p, old_v = struct.unpack_from(self.STRUCT_FMT, self.buffer, offset)
            self._sum_pv -= (old_p / 10000.0) * (old_v / 10000.0)
            self._sum_v -= (old_v / 10000.0)
        else:
            self.size += 1

        struct.pack_into(self.STRUCT_FMT, self.buffer, offset, ts, p_fixed, v_fixed)
        self._sum_pv += price * volume
        self._sum_v += volume
        self.head = (self.head + 1) % self.capacity

    def get_vwap(self) -> float:
        if self._sum_v == 0.0 or self.size == 0:
            return 0.0
        return self._sum_pv / self._sum_v

    def snapshot(self) -> list[Tuple[int, float, float]]:
        entries = []
        for i in range(self.size):
            idx = (self.head - self.size + i) % self.capacity
            offset = idx * self.ENTRY_SIZE
            ts, p, v = struct.unpack_from(self.STRUCT_FMT, self.buffer, offset)
            entries.append((ts, p / 10000.0, v / 10000.0))
        return entries

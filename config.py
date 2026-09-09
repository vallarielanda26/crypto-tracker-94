import os
import json
from collections import ChainMap
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "currency": "USD",
    "update_interval_sec": 15,
    "tracked_assets": ["BTC", "ETH", "SOL"],
    "rpc_nodes": {
        "ETH": "https://eth-mainnet.public.blastapi.io",
        "SOL": "https://api.mainnet-beta.solana.com",
    },
    "alert_threshold_pct": 5.0,
    "max_retries": 3,
}


class DynamicConfig:
    """Flexible configuration proxy with chain-map fallback and env overrides."""

    def __init__(self, filepath: str | None = None):
        self._file_defaults = self._load_file(filepath) if filepath else {}
        self._env_defaults = self._load_env()

    def _load_file(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _load_env(self) -> Dict[str, Any]:
        env_map = {}
        prefix = "CRYPTO_"
        for key, val in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix) :].lower()
                try:
                    env_map[clean_key] = json.loads(val)
                except (json.JSONDecodeError, TypeError):
                    env_map[clean_key] = val
        return env_map

    @property
    def combined(self) -> ChainMap:
        return ChainMap(self._env_defaults, self._file_defaults, DEFAULT_CONFIG)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.combined.get(key, fallback)

    def __getattr__(self, name: str) -> Any:
        if name in self.combined:
            return self.combined[name]
        raise AttributeError(f"Configuration key '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self.combined[item]

    def as_dict(self) -> Dict[str, Any]:
        res = {}
        for map_ in reversed(self.combined.maps):
            res.update(map_)
        return res


config = DynamicConfig(os.getenv("CONFIG_PATH", "config.json"))

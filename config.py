import json
import os
from pathlib import Path
from typing import Any, Dict, NamedTuple


class CryptoConfigDefaults(NamedTuple):
    fiat_currency: str = "USD"
    poll_interval_sec: int = 15
    gas_price_threshold_gwei: float = 50.0
    tracked_assets: tuple = ("BTC", "ETH", "SOL")
    enable_websocket: bool = True
    rpc_endpoints: dict = {
        "ETH": "https://eth-mainnet.g.alchemy.com/v2/demo",
        "SOL": "https://api.mainnet-beta.solana.com",
    }


class ConfigLoader:
    """Cascade configuration loader using environment overrides and dynamic type coercion."""

    ENV_PREFIX = "CRYPTO_"

    def __init__(self, config_path: str | Path | None = None):
        self._defaults = CryptoConfigDefaults()._asdict()
        self._file_config = self._load_file(config_path) if config_path else {}
        self._cached_config: Dict[str, Any] = {}
        self._build()

    def _load_file(self, path: str | Path) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {}
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _cast_env_val(self, val: str, default_val: Any) -> Any:
        if isinstance(default_val, bool):
            return val.lower() in ("true", "1", "yes")
        if isinstance(default_val, int):
            return int(val)
        if isinstance(default_val, float):
            return float(val)
        if isinstance(default_val, tuple):
            return tuple(x.strip() for x in val.split(",") if x.strip())
        if isinstance(default_val, dict):
            try:
                return json.loads(val)
            except json.JSONDecodeError:
                return default_val
        return val

    def _build(self) -> None:
        merged = {**self._defaults, **self._file_config}
        for key, default_val in self._defaults.items():
            env_key = f"{self.ENV_PREFIX}{key.upper()}"
            if env_key in os.environ:
                merged[key] = self._cast_env_val(os.environ[env_key], default_val)
        self._cached_config = merged

    def __getattr__(self, name: str) -> Any:
        if name in self._cached_config:
            return self._cached_config[name]
        raise AttributeError(f"Configuration parameter '{name}' not found")

    def __getitem__(self, item: str) -> Any:
        return self._cached_config[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._cached_config)

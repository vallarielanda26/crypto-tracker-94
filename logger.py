import sys
import logging
import re
from typing import Any, Dict

class SafeCryptoLogger:
    """Resilient logging wrapper that handles edge cases like sensitive key leakage,
    formatting failures, and output stream degradation.
    """
    API_KEY_PATTERN = re.compile(r'(?i)(api[-_]?key|secret|bearer)\s*[:=]\s*["\\']?([a-zA-Z0-9_\-]+)["\\']?')

    def __init__(self, name: str = "crypto_tracker", log_file: str = "tracker.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._setup_handlers(log_file)

    def _setup_handlers(self, log_file: str) -> None:
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except (PermissionError, OSError) as e:
            sys.stderr.write(f"Fallback warning: Failed to create file log handler: {e}\
")

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def _sanitize(self, msg: Any) -> str:
        try:
            text = str(msg)
            return self.API_KEY_PATTERN.sub(r'\1=***REDACTED***', text)
        except Exception:
            return "<unformattable log message>"

    def log_event(self, level: int, msg: Any, *args: Any, **kwargs: Any) -> None:
        try:
            clean_msg = self._sanitize(msg)
            if args:
                clean_args = tuple(self._sanitize(a) for a in args)
                self.logger.log(level, clean_msg, *clean_args, **kwargs)
            else:
                self.logger.log(level, clean_msg, **kwargs)
        except Exception as err:
            try:
                sys.stderr.write(f"[LOGGER EMERGENCY] Failed to write log: {err}\
")
            except Exception:
                pass

    def info(self, msg: Any, *args: Any) -> None:
        self.log_event(logging.INFO, msg, *args)

    def error(self, msg: Any, *args: Any) -> None:
        self.log_event(logging.ERROR, msg, *args)

    def warn(self, msg: Any, *args: Any) -> None:
        self.log_event(logging.WARNING, msg, *args)

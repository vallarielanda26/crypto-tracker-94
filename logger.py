import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class RotatingCryptoLogger:
    def __init__(self, name="crypto-tracker-94", log_path="logs/crypto.log", max_size=1048576, backups=5):
        self.name = name
        self.log_path = log_path
        self.max_size = max_size
        self.backups = backups
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._configure_handlers()

    def _configure_handlers(self):
        rotating_handler = RotatingFileHandler(
            self.log_path,
            maxBytes=self.max_size,
            backupCount=self.backups,
            encoding="utf-8"
        )
        rotating_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        rotating_handler.setFormatter(formatter)
        self.logger.addHandler(rotating_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger

    def track_crypto_event(self, event_type, details):
        log_message = f"CRYPTO_EVENT | {event_type} | {details}"
        self.logger.info(log_message)

    def log_error(self, error_msg, exc=None):
        if exc:
            self.logger.error(f"{error_msg} - {str(exc)}", exc_info=True)
        else:
            self.logger.error(error_msg)

def setup_logger():
    logger_instance = RotatingCryptoLogger()
    return logger_instance.get_logger()

# Usage example integrated
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Crypto tracker started")
    crypto_log = RotatingCryptoLogger()
    crypto_log.track_crypto_event("price_update", "BTC at 65000")
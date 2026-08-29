import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name="crypto_tracker_94", log_dir="logs", max_bytes=1048576, backup_count=5):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, f"{name}.log")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

class CryptoLogger:
    def __init__(self, **config):
        self._logger = setup_logger(**config)
    def info(self, msg):
        self._logger.info(msg)
    def debug(self, msg):
        self._logger.debug(msg)
    def warning(self, msg):
        self._logger.warning(msg)
    def error(self, msg):
        self._logger.error(msg)
    def log_crypto_update(self, coin, price, volume):
        self.info(f"Updated {coin} price: {price} with volume {volume}")
    def log_transaction(self, tx_type, amount, coin):
        self.debug(f"Transaction {tx_type} {amount} {coin}")

if __name__ == "__main__":
    crypto_log = CryptoLogger()
    crypto_log.log_crypto_update("BTC", 67234.56, 1234.5)
    crypto_log.log_transaction("buy", 0.5, "ETH")
    crypto_log.warning("High volatility detected in market")
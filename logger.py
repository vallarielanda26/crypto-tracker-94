import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f'[{datetime.utcnow().isoformat()}Z] {record.msg}'
        return super().format(record)

def setup_crypto_logger(name='crypto-tracker-94'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    path = os.path.join('logs', f'{name}.log')
    handler = RotatingFileHandler(
        path, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    
    formatter = CryptoFormatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

log = setup_crypto_logger()
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

class CryptoFormatter(logging.Formatter):
    def format(self, record):
        record.msg = f"[{datetime.now().isoformat()}] {record.msg}"
        return super().format(record)

def setup_logger(name='crypto-tracker-94', log_file='tracker.log'):
    os.makedirs('logs', exist_ok=True)
    path = os.path.join('logs', log_file)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(CryptoFormatter('%(levelname)s: %(message)s'))
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(CryptoFormatter('%(message)s'))
        logger.addHandler(console)
    
    return logger

logger = setup_logger()
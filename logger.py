import logging
from logging.handlers import RotatingFileHandler

class CryptoEmojiFormatter(logging.Formatter):
    LEVEL_EMOJIS = {
        logging.DEBUG: "🔍",
        logging.INFO: "📈",
        logging.WARNING: "⚠️",
        logging.ERROR: "🚨",
        logging.CRITICAL: "💥"
    }

    def format(self, record):
        emoji = self.LEVEL_EMOJIS.get(record.levelno, "📝")
        record.emoji = emoji
        formatter = logging.Formatter('[%(asctime)s] %(emoji)s %(levelname)s [%(name)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def setup_logger(name="crypto_tracker", log_file="crypto_tracker.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1048576, 
            backupCount=3, 
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = CryptoEmojiFormatter()
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
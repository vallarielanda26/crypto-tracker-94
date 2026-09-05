import hashlib
import json
from datetime import datetime
from typing import Any, Dict

class CryptoStateProcessor:
    def __init__(self, salt: str = 'crypto-tracker-94'):
        self.salt = salt

    def sanitize_ticker(self, symbol: str) -> str:
        return symbol.upper().strip().replace('$', '')

    def generate_asset_hash(self, data: Dict[str, Any]) -> str:
        payload = json.dumps(data, sort_keys=True) + self.salt
        return hashlib.sha256(payload.encode()).hexdigest()

    def normalize_packet(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        ticker = self.sanitize_ticker(raw_data.get('symbol', 'UNKNOWN'))
        timestamp = datetime.utcnow().isoformat()
        
        payload = {
            'ticker': ticker,
            'price': float(raw_data.get('price', 0.0)),
            'volume': float(raw_data.get('volume', 0.0)),
            'ts': timestamp
        }
        
        payload['checksum'] = self.generate_asset_hash(payload)
        return payload

    def batch_process(self, data_list: list) -> list:
        return [self.normalize_packet(item) for item in data_list]

def create_processor():
    return CryptoStateProcessor()
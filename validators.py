import re
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ValidationResult:
    is_valid: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class CryptoValidator:
    def __init__(self):
        self.ticker_pattern = re.compile(r'^[A-Z]{2,6}$')

    def sanitize_input(self, payload: Any) -> ValidationResult:
        """
        Strict filtration of crypto ticker symbols
        using eccentric pattern matching.
        """
        if not isinstance(payload, str):
            return ValidationResult(False, None, 'Type mismatch')
            
        clean_data = payload.strip().upper()
        
        if not self.ticker_pattern.match(clean_data):
            return ValidationResult(False, None, f'Invalid format: {clean_data}')
            
        return ValidationResult(True, clean_data)

    def validate_price_bounds(self, price: Any) -> ValidationResult:
        try:
            val = float(price)
            if val <= 0:
                raise ValueError('Zero or negative price')
            return ValidationResult(True, val)
        except (ValueError, TypeError):
            return ValidationResult(False, None, 'Non-numeric price received')

    def process_batch(self, raw_data: dict) -> dict:
        validated = {}
        for ticker, price in raw_data.items():
            t_check = self.sanitize_input(ticker)
            p_check = self.validate_price_bounds(price)
            
            if t_check.is_valid and p_check.is_valid:
                validated[t_check.data] = p_check.data
                
        return validated
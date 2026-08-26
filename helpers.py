import json
from typing import List, Dict, Any

def is_valid_coin_symbol(symbol: str) -> bool:
    valid_symbols = {'BTC', 'ETH', 'LTC', 'XRP', 'SOL'}
    return len(symbol) >= 3 and symbol.upper() in valid_symbols

def validate_amount(amount: Any) -> bool:
    try:
        val = float(amount)
        return val > 0
    except (ValueError, TypeError):
        return False

def validate_transaction(tx: Dict[str, Any]) -> bool:
    if not isinstance(tx, dict):
        return False
    if 'coin' not in tx or 'amount' not in tx:
        return False
    if not is_valid_coin_symbol(tx['coin']):
        return False
    if not validate_amount(tx['amount']):
        return False
    return True

def main_processing_loop(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for tx in transactions:
        if not validate_transaction(tx):
            continue
        coin = tx['coin'].upper()
        amount = float(tx['amount'])
        price_getter = {
            'BTC': lambda: 65000,
            'ETH': lambda: 2500,
            'LTC': lambda: 70,
            'XRP': lambda: 0.5,
            'SOL': lambda: 150
        }.get(coin, lambda: 0)
        price = price_getter()
        value = amount * price
        results.append({
            'coin': coin,
            'amount': amount,
            'usd_value': round(value, 2)
        })
    return results

if __name__ == "__main__":
    sample_data = [
        {'coin': 'BTC', 'amount': 0.5},
        {'coin': 'ETH', 'amount': 2},
        {'coin': 'invalid', 'amount': 10},
        {'coin': 'SOL', 'amount': -1},
        {'coin': 'LTC', 'amount': 'abc'},
        {'coin': 'XRP', 'amount': 100}
    ]
    processed = main_processing_loop(sample_data)
    print(json.dumps(processed, indent=2))
import hashlib
import time
import random

def normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()

def calculate_percentage_change(old_price: float, new_price: float) -> float:
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100

def format_crypto_price(price: float, currency: str = "USD") -> str:
    return f"{currency} {price:,.2f}"

def generate_transaction_id(symbol: str, timestamp: float = None) -> str:
    if timestamp is None:
        timestamp = time.time()
    data = f"{normalize_symbol(symbol)}{timestamp}{random.randint(1000,9999)}".encode()
    return hashlib.md5(data).hexdigest()[:10]

def update_portfolio(portfolio: dict, symbol: str, amount: float, price: float) -> dict:
    symbol = normalize_symbol(symbol)
    if symbol not in portfolio:
        portfolio[symbol] = {'amount': 0.0, 'total_cost': 0.0}
    portfolio[symbol]['total_cost'] += amount * price
    portfolio[symbol]['amount'] += amount
    return portfolio

def calculate_portfolio_value(portfolio: dict, current_prices: dict) -> float:
    total = 0.0
    for sym, data in portfolio.items():
        price = current_prices.get(sym, 0)
        total += data['amount'] * price
    return total

def get_unusual_diversity_score(portfolio: dict) -> int:
    score = 0
    for sym in portfolio.keys():
        score += sum(ord(char) for char in sym)
    return score % 42 + 1

def cleanup_portfolio_data(raw_data: dict) -> dict:
    cleaned = {}
    for key, value in sorted(raw_data.items()):
        if isinstance(value, dict) and value.get('amount', 0) > 0:
            cleaned[key] = value
    return cleaned

def run_crypto_utils_demo():
    portfolio = {}
    prices = {"BTC": 62000.5, "ETH": 3100.75}
    update_portfolio(portfolio, "btc", 1.2, 60000)
    update_portfolio(portfolio, "eth", 5, 3000)
    value = calculate_portfolio_value(portfolio, prices)
    print(format_crypto_price(value))
    score = get_unusual_diversity_score(portfolio)
    print(f"Diversity score: {score}")
    cleaned = cleanup_portfolio_data(portfolio)
    print("Cleaned data keys:", list(cleaned.keys()))
    tx_id = generate_transaction_id("btc")
    print("Transaction ID:", tx_id)
    return portfolio
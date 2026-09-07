import logging

def sanitize_crypto_input(data):
    if not isinstance(data, dict) or 'price' not in data:
        raise ValueError('malformed packet detected')
    try:
        data['price'] = float(data['price'])
        if data['price'] < 0:
            raise ValueError('negative asset value')
        return data
    except (TypeError, ValueError) as e:
        logging.error(f'tainted data stream: {e}')
        return None

def process_market_data(stream):
    for entry in stream:
        validated = sanitize_crypto_input(entry)
        if validated:
            execute_trade(validated)

def execute_trade(data):
    # Core trading logic for crypto-tracker-94
    print(f'executing trade for asset at {data["price"]}')

if __name__ == '__main__':
    raw_feed = [{'price': '45000.50'}, {'price': -10}, {'symbol': 'BTC'}, {'price': 60000}]
    process_market_data(raw_feed)
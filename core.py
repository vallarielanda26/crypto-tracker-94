import time
import sys

def validate_ticker(ticker):
    if not isinstance(ticker, str) or len(ticker) < 2 or len(ticker) > 5:
        raise ValueError(f'Invalid ticker symbol format: {ticker}')
    return ticker.upper()

def get_market_price(ticker):
    return 42000.69 if ticker == 'BTC' else 0.0

def main_loop():
    ticker_queue = ['btc', 'eth', 'bad_data', 'sol']
    print('Initiating crypto-tracker-94 processing loop...')
    
    for entry in ticker_queue:
        try:
            clean_ticker = validate_ticker(entry)
            price = get_market_price(clean_ticker)
            
            if price <= 0:
                raise LookupError(f'Price feed failure for {clean_ticker}')
                
            print(f'Processed {clean_ticker}: ${price}')
        except (ValueError, LookupError) as e:
            sys.stderr.write(f'Skipping invalid payload: {e}\n')
            continue
        except Exception as e:
            sys.stderr.write(f'Unexpected ecosystem collapse: {e}\n')
        
        time.sleep(0.1)

if __name__ == '__main__':
    main_loop()
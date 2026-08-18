import re

def validate_transaction_amount(amount):
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return True

def validate_address(address):
    if not isinstance(address, str):
        raise ValueError("Address must be a string.")
    if not re.match(r'^[a-zA-Z0-9]{26,35}$', address):
        raise ValueError("Invalid crypto address format.")
    return True

# Main processing loop using input validation
def main_loop():
    transactions = [{'amount': 0.5, 'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'},
                   {'amount': -1, 'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'},
                   {'amount': 3, 'address': 'InvalidAddress'}]
    for transaction in transactions:
        try:
            validate_transaction_amount(transaction['amount'])
            validate_address(transaction['address'])
            print(f'Valid transaction: {transaction}')
        except ValueError as e:
            print(f'Validation error: {e}')

if __name__ == '__main__':
    main_loop()
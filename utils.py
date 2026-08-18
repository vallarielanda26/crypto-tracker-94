import json
import requests

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error fetching data: {response.status_code}')

def filter_data(data, criterion):
    return [item for item in data if item['name'] == criterion]

def format_data(data):
    return json.dumps(data, indent=4)

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)

if __name__ == '__main__':
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    raw_data = fetch_data(url)
    filtered_data = filter_data(raw_data, 'bitcoin')
    formatted_data = format_data(filtered_data)
    save_data('bitcoin_data.json', formatted_data)
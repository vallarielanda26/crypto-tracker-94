# crypto-tracker-94

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

crypto-tracker-94 is a lightweight Python command-line tool that monitors live cryptocurrency prices and calculates portfolio value in real time. It pulls data from public APIs and delivers price alerts directly in the terminal.

## Features
- Fetches real-time prices for 200+ assets via the CoinGecko API
- Calculates total portfolio value using user-defined holdings in JSON format
- Supports threshold-based price alerts with desktop notifications
- Displays 24-hour price changes and basic performance metrics

## Installation

```bash
git clone https://github.com/developer/crypto-tracker-94.git
cd crypto-tracker-94
pip install -r requirements.txt
```

## Usage

Create a `portfolio.json` file:

```json
{
  "BTC": 0.25,
  "ETH": 1.8,
  "SOL": 12
}
```

Run the tracker:

```bash
python main.py --portfolio portfolio.json
```

Set a price alert:

```bash
python main.py --alert BTC 68000
```

## License

MIT License
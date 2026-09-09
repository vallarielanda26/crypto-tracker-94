# crypto-tracker-94

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`crypto-tracker-94` is a lightweight Python library and CLI tool designed for real-time tracking of cryptocurrency prices, market caps, and volume metrics via the CoinGecko API. It allows developers and traders to monitor custom coin watchlists and trigger asynchronous threshold alerts directly within their terminal or python applications.

## Features

- **Asynchronous Data Fetching:** Query spot prices and 24-hour volume for 500+ assets simultaneously with minimal latency using `httpx`.
- **Custom Threshold Alerts:** Set price and percentage-change triggers that log to stdout or push notifications to Discord webhooks.
- **Portfolio P&L Tracking:** Calculate unrealized profit and loss across custom wallet holdings with historical CSV exports.
- **Zero-Config CLI:** Instantly inspect market conditions using simple terminal flags without writing code.

## Installation

Clone the repository and install the dependencies using `pip`:

```bash
git clone https://github.com/Developer/crypto-tracker-94.git
cd crypto-tracker-94
pip install -r requirements.txt
```

## Quick Start

### Python API

```python
from crypto_tracker import Tracker

# Initialize tracker with base currency
tracker = Tracker(currency="usd")

# Fetch current prices
data = tracker.get_spot_price(["bitcoin", "ethereum"])
print(f"BTC: ${data['bitcoin']['price']:,} ({data['bitcoin']['change_24h']:+.2f}%)")

# Set an automated price alert
tracker.add_alert(asset="ethereum", target_price=3500.00, direction="above")
tracker.listen(interval_seconds=30)
```

### Command Line Interface

Check asset prices directly from your shell:

```bash
python -m crypto_tracker --coins bitcoin,solana,cardano --currency usd
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
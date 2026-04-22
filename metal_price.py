#!/usr/bin/env python3
"""
Metal Price Tracker
Fetches live gold and silver spot price and ETFs
from Yahoo Finance.
"""

import json
import urllib.request
import urllib.error
from datetime import datetime

TICKERS = {
    "Silver Spot (SI=F)     ": "SI=F",
    "Gold Spot (GC=F)       ": "GC=F",
    "HDFC Silver ETF        ": "HDFCSILVER.NS",
    "HDFC Gold ETF          ": "HDFCGOLD.NS",
}

BASE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=1d"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
    "Accept": "application/json",
}


def fetch_ticker(ticker_encoded):
    url = BASE_URL.format(ticker_encoded)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    meta = data["chart"]["result"][0]["meta"]
    price = float(meta["regularMarketPrice"])
    prev_close = float(meta["chartPreviousClose"])
    currency = meta.get("currency", "")
    change_pct = ((price - prev_close) / prev_close) * 100
    return price, change_pct, currency


def color(text, code):
    return f"\033[{code}m{text}\033[0m"


def format_price(price, currency):
    symbol = "₹" if currency == "INR" else "$"
    return color(f"{symbol}{price:7.2f}", "97;1")


def format_change(change_pct):
    if change_pct >= 0:
        return color(f"+{change_pct:.2f}%", "92")
    else:
        return color(f"{change_pct:.2f}%", "91")


def main():
    print("\033[H\033[J", end="")
    print(color("Gold and Silver Price", "96;1"), end="")

    timestamp = datetime.now().strftime("%d %b %Y %H:%M:%S")
    lines = [f" {color("[" + timestamp + "]", '90')}"]

    count = 0
    for label, ticker in TICKERS.items():
        try:
            count += 1
            price, change_pct, currency = fetch_ticker(ticker)
            lines.append(
                f"    {color(label, '33')}  "
                f"{format_price(price, currency)}  "
                f"[{format_change(change_pct)}]"
            )
            if count == 2:
                lines.append(f"    {color('-', '33')}  ")
        except urllib.error.URLError as e:
            lines.append(f"    {color(label, '33')}  {color(f'Network error: {e.reason}', '91')}")
        except Exception as e:
            lines.append(f"    {color(label, '33')}  {color(f'Error: {e}', '91')}")
    print("\n".join(lines))

if __name__ == "__main__":
    main()

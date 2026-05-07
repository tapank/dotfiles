#! /usr/bin/python3
import requests
import time
import sys
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"

# Unsorted list of assets
ASSETS = [
    {"name": "HDFC Gold ETF", "ticker": "HDFCGOLD.NS"},
    {"name": "HDFC Silver ETF", "ticker": "HDFCSILVER.NS"},
    {"name": "Silver Futures", "ticker": "SI=F"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS"},
    {"name": "Indian Oil Corporation", "ticker": "IOC.NS"},
    {"name": "HDB Financial Services", "ticker": "HDBFS.NS"},
    {"name": "ITC Ltd.", "ticker": "ITC.NS"},
    {"name": "Infosys Ltd (NASDAQ)", "ticker": "INFY"},
    {"name": "Infosys Ltd (NSE)", "ticker": "INFY.NS"}
]

def clear_screen():
    os.system('clear')

def track_markets():
    results = []
    error_occurred = False
    
    clear_screen()
    print("Loading...")
    
    # Fetch data for all assets before rendering
    for asset in ASSETS:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{asset['ticker']}"
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            meta = response.json()["chart"]["result"][0]["meta"]
            
            price = meta["regularMarketPrice"]
            prev_close = meta["previousClose"]
            gain = ((price - prev_close) / prev_close) * 100
            
            # Extract 52-week metrics and native currency
            high_52 = meta.get("fiftyTwoWeekHigh", price)
            low_52 = meta.get("fiftyTwoWeekLow", price)
            currency = meta.get("currency", "")
            
            results.append({
                "name": asset["name"],
                "ticker": asset["ticker"],
                "price": price,
                "gain": gain,
                "high_52": high_52,
                "low_52": low_52,
                "currency": currency
            })
        except Exception:
            error_occurred = True
            break
    
    if error_occurred:
        print(f"{RED}Error fetching data.")
        return

    clear_screen()
    current_time = datetime.now().strftime("%d %B %Y %I:%M%p")
    
    # Table configuration variables (96 characters wide)
    TABLE_WIDTH = 99
    
    # Print Header
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    print(f"{BOLD}{'LIVE MARKET TRACKER'.center(TABLE_WIDTH)}{RESET}")
    print(f"{YELLOW}{current_time.center(TABLE_WIDTH)}{RESET}")
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    
    # Print Column Headers
    header = f" {'Asset (Ticker)':<36} | {'Spot Price':<14} | {'Daily Gain':<10} | {'52W High':<13} | {'52W Low':<13}"
    print(f"{BOLD}{header}{RESET}")
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    
    # Print Asset Details in Table Rows
    for r in results:
        gain = r["gain"]
        if gain >= 0:
            sign = "+"
            color = GREEN
        else:
            sign = ""
            color = RED
            
        # Format individual strings to guarantee column widths
        name_ticker = f"{r['name']} ({r['ticker']})"
        price_str = f"{r['price']:.2f} {r['currency']}"
        gain_str = f"{sign}{gain:.2f}%"
        high_str = f"{r['high_52']:.2f} {r['currency']}"
        low_str = f"{r['low_52']:.2f} {r['currency']}"
        
        # Construct the row layout using f-string alignment padding
        row = (
            f" {name_ticker:<36} | "
            f"{BOLD}{price_str:<14}{RESET} | "
            f"{color}{gain_str:<10}{RESET} | "
            f"{GREEN}{high_str:<13}{RESET} | "
            f"{RED}{low_str:<13}{RESET}"
        )
        print(row)
        
        # Print Footer
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
            
if __name__ == "__main__":
    track_markets()

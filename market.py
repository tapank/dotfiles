#! /usr/bin/python3
import requests
import sys
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"

# List of assets with specified data sources
ASSETS = [
    {"name": "BSE Sensex", "ticker": "^BSESN", "source": "yahoo"},
    {"name": "Nifty 50", "ticker": "^NSEI", "source": "yahoo"},
    {"name": "HDFC Gold ETF", "ticker": "HDFCGOLD.NS", "source": "yahoo"},
    {"name": "HDFC Silver ETF", "ticker": "HDFCSILVER.NS", "source": "yahoo"},
    {"name": "Silver Futures", "ticker": "SI=F", "source": "yahoo"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS", "source": "yahoo"},
    {"name": "Indian Oil Corporation", "ticker": "IOC.NS", "source": "yahoo"},
    {"name": "HDB Financial Services", "ticker": "HDBFS.NS", "source": "yahoo"}, # Note: Currently unlisted
    {"name": "ITC Ltd.", "ticker": "ITC.NS", "source": "yahoo"},
    {"name": "Infosys Ltd (NASDAQ)", "ticker": "INFY", "source": "yahoo"},
    {"name": "Infosys Ltd (NSE)", "ticker": "INFY.NS", "source": "yahoo"},
    
    # Official AMFI 6-digit scheme codes mapped for the EXACT Regular Growth mutual funds
    {"name": "Axis Liquid Fund", "ticker": "120465", "source": "amfi"},
    {"name": "UTI Nifty 500 Value 50", "ticker": "151738", "source": "amfi"},
    {"name": "HDFC Large Cap Fund", "ticker": "102000", "source": "amfi"},
    {"name": "HDFC Mid Cap Fund", "ticker": "105758", "source": "amfi"},
    {"name": "HDFC NIFTY50 Equal Wgt", "ticker": "148982", "source": "amfi"}
]

def clear_screen():
    os.system('clear')

def track_markets():
    results = []
    failed_tickers = []
    
    clear_screen()
    print("Loading...")
    
    for asset in ASSETS:
        try:
            if asset["source"] == "yahoo":
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{asset['ticker']}"
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
                meta = response.json()["chart"]["result"][0]["meta"]
                
                price = meta["regularMarketPrice"]
                prev_close = meta["previousClose"]
                change = price - prev_close
                gain = (change / prev_close) * 100
                
                high_52 = meta.get("fiftyTwoWeekHigh", price)
                low_52 = meta.get("fiftyTwoWeekLow", price)
                currency = meta.get("currency", "")
                
            elif asset["source"] == "amfi":
                url = f"https://api.mfapi.in/mf/{asset['ticker']}"
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
                
                data = response.json().get("data", [])
                if len(data) < 2:
                    raise Exception("Insufficient NAV data returned from AMFI")
                
                # Fetch latest and previous NAV from official AMFI records
                price = float(data[0]["nav"])
                prev_close = float(data[1]["nav"])
                change = price - prev_close
                gain = (change / prev_close) * 100 if prev_close != 0 else 0
                
                # Approximate 52-week metrics using the last 250 trading days
                navs_1yr = [float(day["nav"]) for day in data[:250]]
                high_52 = max(navs_1yr) if navs_1yr else price
                low_52 = min(navs_1yr) if navs_1yr else price
                currency = "INR"

            results.append({
                "name": asset["name"],
                "ticker": asset["ticker"], 
                "price": price,
                "change": change,
                "gain": gain,
                "high_52": high_52,
                "low_52": low_52,
                "currency": currency
            })
            
        except Exception as e:
            failed_tickers.append(f"{asset['name']} ({type(e).__name__}: {e})")
            continue
    
    clear_screen()
    current_time = datetime.now().strftime("%d %B %Y %I:%M%p")
    TABLE_WIDTH = 112
    
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    print(f"{BOLD}{'LIVE MARKET TRACKER'.center(TABLE_WIDTH)}{RESET}")
    print(f"{YELLOW}{current_time.center(TABLE_WIDTH)}{RESET}")
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    
    header = f" {'Asset (Ticker)':<36} | {'Spot Price':>14} | {'Change':>10} | {'Daily Gain':>10} | {'52W High':>13} | {'52W Low':>13}"
    print(f"{BOLD}{header}{RESET}")
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    
    for r in results:
        gain = r["gain"]
        if gain >= 0:
            sign = "+"
            color = GREEN
        else:
            sign = ""
            color = RED
            
        name_ticker = f"{r['name']} ({r['ticker']})"
        price_str = f"{r['price']:.2f} {r['currency']}"
        change_str = f"{sign}{r['change']:.2f}"
        gain_str = f"{sign}{gain:.2f}%"
        high_str = f"{r['high_52']:.2f} {r['currency']}"
        low_str = f"{r['low_52']:.2f} {r['currency']}"
        
        row = (
            f" {name_ticker:<36} | "
            f"{BOLD}{price_str:>14}{RESET} | "
            f"{color}{change_str:>10}{RESET} | "
            f"{color}{gain_str:>10}{RESET} | "
            f"{GREEN}{high_str:>13}{RESET} | "
            f"{RED}{low_str:>13}{RESET}"
        )
        print(row)
        
    print(f"{CYAN}{'=' * TABLE_WIDTH}{RESET}")
    
    # Print detailed warnings for failed tickers
    if failed_tickers:
        print(f"\n{YELLOW}Note: Unable to fetch data for the following assets:{RESET}")
        for ft in failed_tickers:
            print(f"{YELLOW}  - {ft}{RESET}")
            
if __name__ == "__main__":
    track_markets()
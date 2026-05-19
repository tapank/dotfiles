#! /usr/bin/python3
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# List of assets with specified data sources
ASSETS = [
    {"name": "BSE Sensex", "ticker": "^BSESN", "source": "yahoo"},
    {"name": "Nifty 50", "ticker": "^NSEI", "source": "yahoo"},
    {"name": "HDFC Gold ETF", "ticker": "HDFCGOLD.NS", "source": "yahoo"},
    {"name": "HDFC Silver ETF", "ticker": "HDFCSILVER.NS", "source": "yahoo"},
    {"name": "Silver Futures", "ticker": "SI=F", "source": "yahoo"},
    {"name": "Reliance Industries", "ticker": "RELIANCE.NS", "source": "yahoo"},
    {"name": "Indian Oil Corporation", "ticker": "IOC.NS", "source": "yahoo"},
    {"name": "HDB Financial Services", "ticker": "HDBFS.NS", "source": "yahoo"}, 
    {"name": "ITC Ltd.", "ticker": "ITC.NS", "source": "yahoo"},
    {"name": "Infosys Ltd (NASDAQ)", "ticker": "INFY", "source": "yahoo"},
    {"name": "Infosys Ltd (NSE)", "ticker": "INFY.NS", "source": "yahoo"},
    
    # Official AMFI 6-digit scheme codes
    {"name": "Axis Liquid Fund", "ticker": "112210", "source": "amfi"},
    {"name": "UTI Nifty 500 Value 50", "ticker": "151738", "source": "amfi"},
    {"name": "HDFC Large Cap Fund", "ticker": "102000", "source": "amfi"},
    {"name": "HDFC Mid Cap Fund", "ticker": "105758", "source": "amfi"},
    {"name": "HDFC NIFTY50 Equal Wgt", "ticker": "149106", "source": "amfi"}
]

def track_markets():
    # Clear the screen (compatible with Windows, Mac, and Linux)
    os.system('cls' if os.name == 'nt' else 'clear')
    # force_terminal ensures rich doesn't suppress output if it misreads the TTY state
    console = Console(force_terminal=True)
    results = []
    failed_tickers = []
    
    # Native rich loading spinner replaces os.system('clear')
    with console.status("[bold cyan]Fetching live market data...", spinner="dots"):
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
                    
                    price = float(data[0]["nav"])
                    prev_close = float(data[1]["nav"])
                    change = price - prev_close
                    gain = (change / prev_close) * 100 if prev_close != 0 else 0
                    
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
    
    current_time = datetime.now().strftime("%d %B %Y %I:%M%p")
    
    # Initialize the Rich Table
    table = Table(
        title=f"\n[bold cyan]LIVE MARKET TRACKER[/bold cyan]\n[yellow]{current_time}[/yellow]",
        box=box.ROUNDED,
        header_style="bold cyan",
        title_justify="center"
    )
    
    # Define Columns
    table.add_column("Asset (Ticker)", justify="left", style="bold")
    table.add_column("Spot Price", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("Daily Gain", justify="right")
    table.add_column("52W High", justify="right", style="green")
    table.add_column("52W Low", justify="right", style="red")
    
    # Populate Rows
    for r in results:
        gain = r["gain"]
        if gain >= 0:
            sign = "+"
            color = "green"
        else:
            sign = ""
            color = "red"
            
        name_ticker = f"{r['name']} ({r['ticker']})"
        price_str = f"{r['price']:.2f} {r['currency']}"
        
        # Use Rich markup for inline coloring
        change_str = f"[{color}]{sign}{r['change']:.2f}[/{color}]"
        gain_str = f"[{color}]{sign}{gain:.2f}%[/{color}]"
        
        high_str = f"{r['high_52']:.2f} {r['currency']}"
        low_str = f"{r['low_52']:.2f} {r['currency']}"
        
        table.add_row(name_ticker, price_str, change_str, gain_str, high_str, low_str)
        
    # Render the table to the terminal
    console.print(table)
    
    # Print detailed warnings for failed tickers
    if failed_tickers:
        console.print("\n[yellow]Note: Unable to fetch data for the following assets:[/yellow]")
        for ft in failed_tickers:
            console.print(f"[yellow]  - {ft}[/yellow]")
            
if __name__ == "__main__":
    track_markets()

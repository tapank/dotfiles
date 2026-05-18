#!/usr/bin/env python3
import os
import datetime
import requests
from rich.console import Console, Group
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich import box

# Define the coordinates for the locations
LOCATIONS = {
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Tampa": {"lat": 27.9506, "lon": -82.4572}
}

def fetch_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,rain,weather_code",
        "hourly": "temperature_2m,precipitation_probability",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 7
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def build_city_panel(location_name, data):
    """Builds a styled, colored Rich panel for a single city."""
    if not data:
        return Panel(f"[red]Error fetching data for {location_name}[/]", title=location_name)

    # 1. Current Conditions
    current = data.get("current", {})
    c_temp = current.get("temperature_2m", "--")
    c_rain = current.get("rain", "--")
    current_time_str = current.get("time") # Gets the current local time from the API
    
    current_str = f"[bold yellow]Current:[/] [green]{c_temp}°C[/] | [bold cyan]Rain:[/] {c_rain} mm\n"

    # 2. Hourly Forecast Table
    hourly = data.get("hourly", {})
    hourly_table = Table(box=box.SIMPLE, show_edge=False, padding=(0, 1))
    hourly_table.add_column("Time", style="dim")
    hourly_table.add_column("Temp", justify="right")
    hourly_table.add_column("Rain", justify="right", style="cyan")

    # Find the index of the current local hour to show the *next* 4 hours
    start_idx = 0
    if current_time_str:
        current_time_obj = datetime.datetime.fromisoformat(current_time_str)
        # Round to the current hour to match Open-Meteo's hourly timestamp format
        current_hour_str = current_time_obj.strftime("%Y-%m-%dT%H:00")
        try:
            start_idx = hourly["time"].index(current_hour_str)
        except ValueError:
            start_idx = 0

    # Grab the next 4 hours starting from the current local hour
    for i in range(start_idx, start_idx + 4):
        raw_time = hourly["time"][i]
        time_str = datetime.datetime.fromisoformat(raw_time).strftime("%I:%M %p")
        temp = f"{hourly['temperature_2m'][i]}°C"
        prob = f"{hourly['precipitation_probability'][i]}%"
        hourly_table.add_row(time_str, temp, prob)

    # 3. Daily Forecast Table
    daily = data.get("daily", {})
    daily_table = Table(box=box.SIMPLE, show_edge=False, padding=(0, 1))
    daily_table.add_column("Date", style="dim")
    daily_table.add_column("Max / Min") # Swapped header
    daily_table.add_column("Rain", justify="right", style="cyan")

    for i in range(7):
        raw_date = daily["time"][i]
        date_str = datetime.datetime.strptime(raw_date, "%Y-%m-%d").strftime("%a, %b %d")
        
        min_temp = daily["temperature_2m_min"][i]
        max_temp = daily["temperature_2m_max"][i]
        rain_chance = daily["precipitation_probability_max"][i]
        
        # Swapped layout: Max first (Red), then Min (Blue)
        temp_range = f"[red]{max_temp}°[/] / [blue]{min_temp}°[/]"
        daily_table.add_row(date_str, temp_range, f"{rain_chance}%")

    # Combine everything into a single layout group
    content = Group(
        current_str,
        "[bold underline]Hourly (Next 4h)[/]",
        hourly_table,
        "",
        "[bold underline]7-Day Forecast[/]",
        daily_table
    )

    # Wrap it in a beautiful bordered panel
    return Panel(content, title=f"[bold white]{location_name}[/]", border_style="bright_blue", expand=True)

def main():
    # Clear the screen (compatible with Windows, Mac, and Linux)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console = Console()
    
    # Use a loading spinner while fetching data
    with console.status("[bold green]Fetching latest weather data...[/]", spinner="dots"):
        panels = []
        for name, coords in LOCATIONS.items():
            data = fetch_weather(coords["lat"], coords["lon"])
            panels.append(build_city_panel(name, data))
    
    # Display the panels side-by-side in columns
    console.print()
    console.print(Columns(panels, equal=True))
    console.print()

if __name__ == "__main__":
    main()
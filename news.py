#!/usr/bin/env python3

import webbrowser
import urllib.request
import xml.etree.ElementTree as ET
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList
from textual.widgets.option_list import Option
from textual.containers import Horizontal

# The curated dictionary of feeds
# The curated dictionary of feeds
FEEDS = {
    "World News (NYT)": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "World News (Al Jazeera)": "https://www.aljazeera.com/xml/rss/all.xml",
    "National News": "https://www.thehindu.com/news/national/?service=rss",
    "Indian Markets": "https://www.livemint.com/rss/money",
    "Cricket News": "https://www.espncricinfo.com/rss/content/story/feeds/0.xml",
    "Linux & Open Source": "https://www.phoronix.com/rss.php",
}

class NewsReaderApp(App):
    """A Textual App with a sidebar to switch between news feeds."""

    CSS = """
    Horizontal {
        height: 1fr;
    }

    #sidebar {
        width: 30;
        border: round $accent;
        height: 1fr;
        margin: 1 1 1 2;
    }

    #headline_list {
        border: round $accent;
        height: 1fr;
        margin: 1 2 1 1;
    }
    
    /* Highlight the active pane to show which list has focus */
    OptionList:focus {
        border: round $success;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Feed"),
        ("h", "focus_sidebar", "Left (Feeds)"),
        ("l", "focus_headlines", "Right (Headlines)"),
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
    ]

    def __init__(self):
        super().__init__()
        self.news_items = []
        self.current_feed_name = list(FEEDS.keys())[0]
        self.current_feed_url = FEEDS[self.current_feed_name]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            # Populate the sidebar directly from the dictionary keys
            yield OptionList(*[Option(name) for name in FEEDS.keys()], id="sidebar")
            yield OptionList(id="headline_list")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Terminal News Reader"
        
        # Select the first feed in the sidebar and focus it
        sidebar = self.query_one("#sidebar")
        sidebar.highlighted = 0
        sidebar.focus()
        
        self.fetch_news()

    def action_refresh(self) -> None:
        self.fetch_news()

    def action_focus_sidebar(self) -> None:
        self.query_one("#sidebar").focus()

    def action_focus_headlines(self) -> None:
        self.query_one("#headline_list").focus()

    def action_cursor_down(self) -> None:
        # Determine which list currently has focus
        active_list = self.focused if isinstance(self.focused, OptionList) else self.query_one("#sidebar")
        
        if active_list.highlighted is None:
            active_list.highlighted = 0
        elif active_list.highlighted < active_list.option_count - 1:
            active_list.highlighted += 1

    def action_cursor_up(self) -> None:
        active_list = self.focused if isinstance(self.focused, OptionList) else self.query_one("#sidebar")
        
        if active_list.highlighted is not None and active_list.highlighted > 0:
            active_list.highlighted -= 1

    def fetch_news(self) -> None:
        headline_list = self.query_one("#headline_list")
        headline_list.clear_options()
        self.news_items = []
        self.sub_title = f"Fetching {self.current_feed_name}..."
        
        try:
            req = urllib.request.Request(self.current_feed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
            
            root = ET.fromstring(xml_data)
            
            # Using .//item handles slight variations in different RSS architectures
            for item in root.findall('.//item')[:20]:  
                title_elem = item.find('title')
                link_elem = item.find('link')
                
                if title_elem is not None and link_elem is not None:
                    title = title_elem.text.strip() if title_elem.text else "No Title"
                    link = link_elem.text.strip() if link_elem.text else ""
                    self.news_items.append({"title": title, "link": link})
                    headline_list.add_option(Option(title))
                
            self.sub_title = f"{self.current_feed_name} | 'Enter' to open | 'h'/'l' to switch panes"
                
        except Exception as e:
            self.sub_title = f"Failed to fetch {self.current_feed_name}."
            headline_list.add_option(Option(f"Error: {e}"))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # Determine which OptionList was clicked or pressed Enter on
        if event.option_list.id == "sidebar":
            self.current_feed_name = str(event.option.prompt)
            self.current_feed_url = FEEDS[self.current_feed_name]
            self.fetch_news()
            
            # Automatically jump focus to the right so you can immediately scroll headlines
            self.query_one("#headline_list").focus()
            
        elif event.option_list.id == "headline_list":
            index = event.option_index
            if index < len(self.news_items):
                url = self.news_items[index]["link"]
                webbrowser.open(url)
                self.notify(f"Opening browser...", title="Success")

if __name__ == "__main__":
    app = NewsReaderApp()
    app.run()

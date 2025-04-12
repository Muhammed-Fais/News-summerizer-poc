import requests
import feedparser
from src.config import NEWS_CONFIG

def fetch_news(rss_url, entries=5):
    """Fetch news from a single RSS feed."""
    try:
        headers = {"User-Agent": "NewsSummarizerPOC/1.0"}
        response = requests.get(rss_url, timeout=10, headers=headers)
        response.raise_for_status()
        feed = feedparser.parse(response.content)

        if not feed.entries:
            print(f"Warning: No entries found in RSS feed: {rss_url}")
            return "No news available from this source.\n"
        
        news = ""
        for entry in feed.entries[:entries]:
            news += f"{entry.title} (Source: {entry.link}) {entry.description}\n"

        return news
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed {rss_url}: {e}")
        return f"Failed to fetch news due to: {e}\n"

def get_all_news(category=None):
    """Collect news from all or specified category sources without truncation."""
    news = ""
    sources = NEWS_CONFIG["sources"]
    
    if category and category.lower() in sources:

        news += f"\n{category.capitalize()} News:\n{fetch_news(sources[category.lower()], NEWS_CONFIG['n_items'])}"
    else:

        for topic, url in sources.items():
            news += f"\n{topic.capitalize()} News:\n{fetch_news(url, NEWS_CONFIG['n_items'])}"

    return news
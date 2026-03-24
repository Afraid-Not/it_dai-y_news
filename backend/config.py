import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./news.db")
COLLECT_HOUR = int(os.getenv("COLLECT_HOUR", "7"))
COLLECT_MINUTE = int(os.getenv("COLLECT_MINUTE", "0"))

RSS_SOURCES = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
}

HACKERNEWS_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HACKERNEWS_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HACKERNEWS_FETCH_COUNT = 15

GEEKNEWS_URL = "https://news.hada.io/rss"

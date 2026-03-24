import feedparser
import httpx
from datetime import datetime
from email.utils import parsedate_to_datetime
from config import RSS_SOURCES


def _parse_date(entry) -> datetime | None:
    published = entry.get("published") or entry.get("updated")
    if not published:
        return None
    try:
        return parsedate_to_datetime(published)
    except Exception:
        return None


async def fetch_rss() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=30) as client:
        for source_name, feed_url in RSS_SOURCES.items():
            try:
                resp = await client.get(feed_url)
                feed = feedparser.parse(resp.text)
                for entry in feed.entries[:10]:
                    articles.append({
                        "title": entry.get("title", ""),
                        "url": entry.get("link", ""),
                        "source": source_name,
                        "published_at": _parse_date(entry),
                    })
            except Exception:
                continue
    return articles

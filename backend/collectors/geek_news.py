import feedparser
import httpx
from datetime import datetime
from email.utils import parsedate_to_datetime
from config import GEEKNEWS_URL


def _parse_date(entry) -> datetime | None:
    published = entry.get("published") or entry.get("updated")
    if not published:
        return None
    try:
        return parsedate_to_datetime(published)
    except Exception:
        return None


async def fetch_geeknews() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.get(GEEKNEWS_URL)
            feed = feedparser.parse(resp.text)
            for entry in feed.entries[:15]:
                articles.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "source": "GeekNews",
                    "published_at": _parse_date(entry),
                })
        except Exception:
            pass
    return articles

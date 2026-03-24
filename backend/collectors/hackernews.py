import httpx
from config import HACKERNEWS_TOP_URL, HACKERNEWS_ITEM_URL, HACKERNEWS_FETCH_COUNT


async def fetch_hackernews() -> list[dict]:
    articles = []
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(HACKERNEWS_TOP_URL)
        story_ids = resp.json()[:HACKERNEWS_FETCH_COUNT]

        for story_id in story_ids:
            try:
                item_resp = await client.get(HACKERNEWS_ITEM_URL.format(story_id))
                item = item_resp.json()
                if item and item.get("url"):
                    articles.append({
                        "title": item.get("title", ""),
                        "url": item["url"],
                        "source": "Hacker News",
                        "published_at": None,
                    })
            except Exception:
                continue
    return articles

from datetime import datetime
from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from collectors.hackernews import fetch_hackernews
from collectors.rss_collector import fetch_rss
from collectors.geek_news import fetch_geeknews
from services.summarizer import summarize_articles
from models.news import News
from database import get_session

scheduler = AsyncIOScheduler()


async def collect_and_summarize():
    print(f"[{datetime.now()}] 뉴스 수집 시작...")

    # 1. 수집
    hn_articles = await fetch_hackernews()
    rss_articles = await fetch_rss()
    geek_articles = await fetch_geeknews()
    all_articles = hn_articles + rss_articles + geek_articles
    print(f"수집된 기사: {len(all_articles)}개")

    # 2. 중복 제거 (URL 기준)
    async with get_session() as session:
        existing = await session.execute(select(News.original_url))
        existing_urls = {row[0] for row in existing.fetchall()}

    new_articles = [a for a in all_articles if a["url"] not in existing_urls]
    print(f"신규 기사: {len(new_articles)}개")

    if not new_articles:
        print("새로운 기사가 없습니다.")
        return

    # 3. AI 요약
    summarized = await summarize_articles(new_articles)
    print(f"요약 완료: {len(summarized)}개")

    # 4. DB 저장
    async with get_session() as session:
        for item in summarized:
            news = News(
                title=item["title"],
                summary_ko=item["summary_ko"],
                category=item["category"],
                source=item["source"],
                original_url=item["original_url"],
                published_at=item.get("published_at"),
            )
            session.add(news)
        await session.commit()

    print(f"[{datetime.now()}] 뉴스 수집 완료! {len(summarized)}개 저장")


def start_scheduler(hour: int, minute: int):
    scheduler.add_job(
        collect_and_summarize,
        "cron",
        hour=hour,
        minute=minute,
        id="daily_news_collect",
        replace_existing=True,
    )
    scheduler.start()
    print(f"스케줄러 시작: 매일 {hour:02d}:{minute:02d}에 수집 실행")

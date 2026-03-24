from datetime import date, datetime, timedelta
from fastapi import APIRouter, Query
from sqlalchemy import select, func
from database import get_session
from models.news import News

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/")
async def get_news(
    target_date: date | None = Query(None, description="조회 날짜 (YYYY-MM-DD)"),
    category: str | None = Query(None, description="카테고리 필터"),
):
    if target_date is None:
        target_date = date.today()

    start = datetime.combine(target_date, datetime.min.time())
    end = start + timedelta(days=1)

    async with get_session() as session:
        query = select(News).where(
            News.collected_at >= start,
            News.collected_at < end,
        ).order_by(News.collected_at.desc())

        if category:
            query = query.where(News.category == category)

        result = await session.execute(query)
        news_list = result.scalars().all()

    return {
        "date": target_date.isoformat(),
        "count": len(news_list),
        "articles": [n.to_dict() for n in news_list],
    }


@router.get("/categories")
async def get_categories():
    async with get_session() as session:
        result = await session.execute(
            select(News.category, func.count(News.id))
            .group_by(News.category)
        )
        categories = [{"name": row[0], "count": row[1]} for row in result.fetchall()]
    return {"categories": categories}


@router.get("/dates")
async def get_available_dates():
    async with get_session() as session:
        result = await session.execute(
            select(func.date(News.collected_at))
            .distinct()
            .order_by(func.date(News.collected_at).desc())
            .limit(30)
        )
        dates = [row[0] for row in result.fetchall()]
    return {"dates": dates}

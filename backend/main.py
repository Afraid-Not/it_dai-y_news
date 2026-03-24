from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.news import router as news_router
from services.scheduler import start_scheduler, collect_and_summarize
from config import COLLECT_HOUR, COLLECT_MINUTE


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    start_scheduler(COLLECT_HOUR, COLLECT_MINUTE)
    yield


app = FastAPI(title="IT Daily News", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router)


@app.get("/")
async def root():
    return {"message": "IT Daily News API", "docs": "/docs"}


@app.post("/api/collect")
async def trigger_collect():
    """수동으로 뉴스 수집 트리거"""
    await collect_and_summarize()
    return {"message": "수집 완료"}

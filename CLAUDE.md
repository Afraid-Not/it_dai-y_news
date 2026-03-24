# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IT Daily News — a full-stack app that automatically collects IT news from multiple sources, summarizes them in Korean via OpenAI (gpt-4o-mini), and displays them in a web dashboard. News is collected daily on a cron schedule (default 07:00) or manually via API/UI button.

## Architecture

**Monorepo with two independent stacks:**

- `backend/` — Python, FastAPI, async SQLAlchemy (aiosqlite/SQLite), APScheduler
- `frontend/` — Next.js 15 (App Router, Turbopack), React 19, Tailwind CSS 4

**Data flow:** Collectors gather articles → Scheduler deduplicates by URL → Summarizer batches to OpenAI for Korean translation/summary/categorization → Stored in SQLite → Served via REST API → Frontend fetches and renders.

**Frontend→Backend proxy:** Next.js `rewrites` in `next.config.ts` proxies `/api/*` to `http://localhost:8000/api/*`. Both servers must run simultaneously during development.

### Backend structure

- `main.py` — FastAPI app with lifespan (init DB + start scheduler), CORS, manual collect endpoint (`POST /api/collect`)
- `config.py` — env vars and source configuration (RSS feeds, HackerNews, GeekNews URLs)
- `database.py` — async SQLAlchemy engine and session factory
- `models/news.py` — single `News` model (title, summary_ko, category, source, original_url, published_at, collected_at)
- `collectors/` — three async collectors: `hackernews.py`, `rss_collector.py`, `geek_news.py`
- `services/scheduler.py` — APScheduler cron job + `collect_and_summarize()` orchestration (collect → dedupe → summarize → save)
- `services/summarizer.py` — OpenAI batch summarization (10 articles per batch, JSON response format)
- `routers/news.py` — REST endpoints: `GET /api/news/` (by date + optional category), `GET /api/news/categories`, `GET /api/news/dates`

### News categories

AI, 보안, 클라우드, 개발, 스타트업, 하드웨어, 기타 — assigned by GPT during summarization.

## Development Commands

### Backend

```bash
cd backend
# Environment setup (conda + uv)
conda create -n it-daily-news python=3.12
conda activate it-daily-news
uv pip install -r requirements.txt

# Run (from backend/ directory)
uvicorn main:app --reload --port 8000

# API docs available at http://localhost:8000/docs
```

Requires `OPENAI_API_KEY` in `backend/.env` (see `.env.example`).

### Frontend

```bash
cd frontend
npm install

# Dev server with Turbopack
npm run dev        # http://localhost:3000

# Production build
npm run build
npm start
```

### Running both together

Start backend (port 8000) and frontend (port 3000) in separate terminals. The frontend proxies API calls to the backend automatically.

## Key Details

- DB is SQLite file at `backend/news.db`, auto-created on first run
- Article deduplication uses `original_url` (unique constraint)
- Summarizer is synchronous OpenAI client (not async) despite being called from async context
- No test suite exists yet
- No linter/formatter configured
- UI is Korean-language throughout

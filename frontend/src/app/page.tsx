"use client";

import { useEffect, useState } from "react";
import NewsCard, { type Article } from "@/components/NewsCard";
import CategoryFilter from "@/components/CategoryFilter";
import DatePicker from "@/components/DatePicker";

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr);
  return d.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  });
};

const Home = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [category, setCategory] = useState("전체");
  const [date, setDate] = useState(
    () => new Date().toISOString().split("T")[0],
  );
  const [loading, setLoading] = useState(true);
  const [collecting, setCollecting] = useState(false);

  const fetchNews = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ target_date: date });
      if (category !== "전체") params.set("category", category);
      const res = await fetch(`/api/news?${params}`);
      const data = await res.json();
      setArticles(data.articles || []);
    } catch {
      setArticles([]);
    } finally {
      setLoading(false);
    }
  };

  const triggerCollect = async () => {
    setCollecting(true);
    try {
      await fetch("/api/collect", { method: "POST" });
      await fetchNews();
    } finally {
      setCollecting(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, [date, category]);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <header className="mb-8">
        <h1 className="mb-1 text-3xl font-bold">IT Daily News</h1>
        <p className="text-sm text-[var(--text-secondary)]">
          AI가 매일 아침 정리해주는 IT 뉴스
        </p>
      </header>

      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <DatePicker value={date} onChange={setDate} />
        <button
          onClick={triggerCollect}
          disabled={collecting}
          className="rounded-lg bg-[var(--accent)] px-4 py-1.5 text-sm font-medium text-white transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {collecting ? "수집 중..." : "지금 수집하기"}
        </button>
      </div>

      <div className="mb-6">
        <CategoryFilter selected={category} onSelect={setCategory} />
      </div>

      <p className="mb-4 text-sm text-[var(--text-secondary)]">
        {formatDate(date)} &middot; {articles.length}개 기사
      </p>

      {loading ? (
        <div className="py-20 text-center text-[var(--text-secondary)]">
          불러오는 중...
        </div>
      ) : articles.length === 0 ? (
        <div className="py-20 text-center text-[var(--text-secondary)]">
          <p className="mb-2">이 날짜에 수집된 뉴스가 없습니다.</p>
          <p className="text-xs">
            &quot;지금 수집하기&quot; 버튼을 눌러 뉴스를 가져와보세요.
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {articles.map((article) => (
            <NewsCard key={article.id} article={article} />
          ))}
        </div>
      )}
    </main>
  );
};

export default Home;

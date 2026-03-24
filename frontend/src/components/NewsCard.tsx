"use client";

interface Article {
  id: number;
  title: string;
  summary_ko: string;
  category: string;
  source: string;
  original_url: string;
  published_at: string | null;
  collected_at: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  AI: "bg-purple-500/20 text-purple-400",
  보안: "bg-red-500/20 text-red-400",
  클라우드: "bg-sky-500/20 text-sky-400",
  개발: "bg-green-500/20 text-green-400",
  스타트업: "bg-yellow-500/20 text-yellow-400",
  하드웨어: "bg-orange-500/20 text-orange-400",
  기타: "bg-gray-500/20 text-gray-400",
};

const NewsCard = ({ article }: { article: Article }) => {
  const colorClass =
    CATEGORY_COLORS[article.category] || CATEGORY_COLORS["기타"];

  return (
    <a
      href={article.original_url}
      target="_blank"
      rel="noopener noreferrer"
      className="block rounded-xl border border-[var(--border)] bg-[var(--bg-card)] p-5 transition-colors hover:bg-[var(--bg-card-hover)]"
    >
      <div className="mb-3 flex items-center gap-2">
        <span
          className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${colorClass}`}
        >
          {article.category}
        </span>
        <span className="text-xs text-[var(--text-secondary)]">
          {article.source}
        </span>
      </div>
      <h3 className="mb-2 text-lg font-semibold leading-snug">
        {article.title}
      </h3>
      <p className="text-sm leading-relaxed text-[var(--text-secondary)]">
        {article.summary_ko}
      </p>
    </a>
  );
};

export default NewsCard;
export type { Article };

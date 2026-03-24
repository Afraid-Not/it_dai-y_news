"use client";

const CATEGORIES = [
  "전체",
  "AI",
  "보안",
  "클라우드",
  "개발",
  "스타트업",
  "하드웨어",
  "기타",
];

const CategoryFilter = ({
  selected,
  onSelect,
}: {
  selected: string;
  onSelect: (cat: string) => void;
}) => {
  return (
    <div className="flex flex-wrap gap-2">
      {CATEGORIES.map((cat) => (
        <button
          key={cat}
          onClick={() => onSelect(cat)}
          className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
            selected === cat
              ? "bg-[var(--accent)] text-white"
              : "bg-[var(--bg-card)] text-[var(--text-secondary)] hover:bg-[var(--bg-card-hover)]"
          }`}
        >
          {cat}
        </button>
      ))}
    </div>
  );
};

export default CategoryFilter;

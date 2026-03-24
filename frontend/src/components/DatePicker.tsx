"use client";

const DatePicker = ({
  value,
  onChange,
}: {
  value: string;
  onChange: (date: string) => void;
}) => {
  return (
    <input
      type="date"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] px-3 py-1.5 text-sm text-[var(--text-primary)] outline-none focus:border-[var(--accent)]"
    />
  );
};

export default DatePicker;

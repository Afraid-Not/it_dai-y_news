import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IT Daily News",
  description: "매일 아침 AI가 정리해주는 IT 뉴스",
};

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
};

export default RootLayout;

import json
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """당신은 IT 뉴스 전문 편집자입니다. 주어진 뉴스 기사 제목과 URL 목록을 보고 다음을 수행합니다:
1. 각 기사의 제목을 한국어로 번역
2. 기사 내용을 3~4줄로 한국어 요약
3. 카테고리 분류 (AI, 보안, 클라우드, 개발, 스타트업, 하드웨어, 기타 중 하나)

반드시 아래 JSON 형식으로 응답하세요:
[
  {
    "title": "한국어 번역된 제목",
    "summary_ko": "한국어 요약 (3~4줄)",
    "category": "카테고리"
  }
]
"""


async def summarize_articles(articles: list[dict]) -> list[dict]:
    if not articles:
        return []

    batch_size = 10
    results = []

    for i in range(0, len(articles), batch_size):
        batch = articles[i:i + batch_size]
        user_content = "\n".join(
            f"{idx + 1}. [{a['source']}] {a['title']} - {a['url']}"
            for idx, a in enumerate(batch)
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT + "\n\n최상위 키 'articles'로 배열을 감싸서 JSON 객체로 응답하세요."},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=4096,
            )

            response_text = response.choices[0].message.content or ""
            parsed = json.loads(response_text)
            summaries = parsed.get("articles", parsed) if isinstance(parsed, dict) else parsed

            for idx, summary in enumerate(summaries):
                if idx < len(batch):
                    results.append({
                        "title": summary.get("title", batch[idx]["title"]),
                        "summary_ko": summary.get("summary_ko", ""),
                        "category": summary.get("category", "기타"),
                        "source": batch[idx]["source"],
                        "original_url": batch[idx]["url"],
                        "published_at": batch[idx].get("published_at"),
                    })
        except Exception as e:
            print(f"Summarization error: {e}")
            for a in batch:
                results.append({
                    "title": a["title"],
                    "summary_ko": "요약 실패",
                    "category": "기타",
                    "source": a["source"],
                    "original_url": a["url"],
                    "published_at": a.get("published_at"),
                })

    return results

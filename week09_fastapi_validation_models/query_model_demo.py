from dataclasses import dataclass
from typing import Optional


@dataclass
class ArticleFilter:
    keyword: Optional[str] = None
    limit: int = 10
    offset: int = 0
    order_by: str = "created_at"

    def validate(self) -> "ArticleFilter":
        if self.keyword is not None and len(self.keyword.strip()) < 2:
            raise ValueError("keyword는 2글자 이상이어야 합니다.")
        if not 1 <= self.limit <= 50:
            raise ValueError("limit은 1부터 50 사이여야 합니다.")
        if self.offset < 0:
            raise ValueError("offset은 0 이상이어야 합니다.")
        if self.order_by not in {"created_at", "title", "views"}:
            raise ValueError("order_by 값이 허용 범위를 벗어났습니다.")
        return self


ARTICLES = [
    {"id": 1, "title": "FastAPI validation", "views": 120, "created_at": "2026-04-29"},
    {"id": 2, "title": "Query model pattern", "views": 90, "created_at": "2026-05-01"},
    {"id": 3, "title": "Pydantic field rule", "views": 150, "created_at": "2026-05-03"},
]


def search_articles(params: ArticleFilter) -> list[dict]:
    params.validate()
    rows = ARTICLES
    if params.keyword:
        keyword = params.keyword.lower()
        rows = [row for row in rows if keyword in row["title"].lower()]
    rows = sorted(rows, key=lambda row: row[params.order_by])
    return rows[params.offset : params.offset + params.limit]


if __name__ == "__main__":
    result = search_articles(ArticleFilter(keyword="api", limit=5, order_by="views"))
    print(result)

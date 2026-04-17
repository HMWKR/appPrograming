"""실습과제 2 — create 모듈: C (Create/Insert).

- insert_one:   단일 행 삽입
- insert_many:  튜플 리스트 일괄 삽입 (executemany)
- load_from_csv: CSV URL에서 상위 N개 로드 후 일괄 삽입
"""

from __future__ import annotations

import sqlite3
from typing import Iterable

import pandas as pd

from init import connect

CSV_URL = "https://raw.githubusercontent.com/ancestor9/data/main/customers.csv"


def insert_one(conn: sqlite3.Connection, username: str, full_name: str) -> None:
    """단일 고객 삽입. UNIQUE 제약 위반 시 IntegrityError 발생."""
    conn.execute(
        "INSERT INTO customers (username, full_name) VALUES (?, ?)",
        (username, full_name),
    )
    conn.commit()


def insert_many(conn: sqlite3.Connection, rows: Iterable[tuple[str, str]]) -> int:
    """튜플(username, full_name) 리스트를 일괄 삽입. UNIQUE 충돌은 무시."""
    rows = list(rows)
    conn.executemany(
        "INSERT OR IGNORE INTO customers (username, full_name) VALUES (?, ?)",
        rows,
    )
    conn.commit()
    return len(rows)


def load_from_csv(
    conn: sqlite3.Connection,
    url: str = CSV_URL,
    limit: int = 10,
) -> int:
    """CSV에서 상위 limit개를 읽어 삽입. 강의 예제(Cell 13)와 동일 전략."""
    df = pd.read_csv(url).head(limit)
    if "고객ID" not in df.columns:
        raise KeyError(f"'고객ID' 컬럼 없음. 실제 컬럼: {list(df.columns)}")
    rows = [(str(v), str(v)) for v in df["고객ID"].tolist()]
    return insert_many(conn, rows)


if __name__ == "__main__":
    conn = connect()
    n = load_from_csv(conn, limit=10)
    print(f"[create] CSV 상위 10개 요청 → {n}개 시도 (중복은 무시)")
    conn.close()

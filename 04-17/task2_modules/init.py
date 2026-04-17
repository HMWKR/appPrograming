"""실습과제 2 — init 모듈: DB 파일 초기화 + customers 테이블 생성."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "customer_data.db"


def connect() -> sqlite3.Connection:
    """DB 파일에 연결. 없으면 sqlite3가 자동 생성한다."""
    return sqlite3.connect(DB_PATH)


def reset_db() -> None:
    """기존 DB 파일을 삭제해 완전 초기 상태로 돌린다."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def create_table(conn: sqlite3.Connection) -> None:
    """customers 테이블을 생성(없을 때만)."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT NOT NULL UNIQUE,
            full_name TEXT
        )
        """
    )
    conn.commit()


def init_db(fresh: bool = True) -> sqlite3.Connection:
    """DB 전체 초기화 루틴. fresh=True면 파일부터 재생성."""
    if fresh:
        reset_db()
    conn = connect()
    create_table(conn)
    return conn


if __name__ == "__main__":
    conn = init_db(fresh=True)
    print(f"[init] {DB_PATH} 생성 + customers 테이블 준비 완료")
    conn.close()

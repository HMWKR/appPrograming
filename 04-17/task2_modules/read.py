"""실습과제 2 — read 모듈: R (Read/Select)."""

from __future__ import annotations

import sqlite3

from init import connect


def fetch_all(conn: sqlite3.Connection) -> list[tuple]:
    """id 오름차순으로 전체 고객 조회."""
    return conn.execute(
        "SELECT id, username, full_name FROM customers ORDER BY id"
    ).fetchall()


def fetch_by_username(conn: sqlite3.Connection, username: str) -> tuple | None:
    """username으로 단건 조회. 없으면 None."""
    return conn.execute(
        "SELECT id, username, full_name FROM customers WHERE username = ?",
        (username,),
    ).fetchone()


def count(conn: sqlite3.Connection) -> int:
    """총 행 수."""
    return conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]


if __name__ == "__main__":
    conn = connect()
    print(f"[read] 총 {count(conn)}행")
    for row in fetch_all(conn):
        print("  ", row)
    print("---")
    print("[read] CUST_0002 →", fetch_by_username(conn, "CUST_0002"))
    conn.close()

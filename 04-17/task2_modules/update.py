"""실습과제 2 — update 모듈: U (Update)."""

from __future__ import annotations

import sqlite3

from init import connect


def update_full_name(
    conn: sqlite3.Connection, username: str, new_full_name: str
) -> int:
    """특정 username의 full_name을 수정. 반환: 변경된 행 수."""
    cur = conn.execute(
        "UPDATE customers SET full_name = ? WHERE username = ?",
        (new_full_name, username),
    )
    conn.commit()
    return cur.rowcount


if __name__ == "__main__":
    conn = connect()
    n = update_full_name(conn, "CUST_0002", "Updated User 02")
    print(f"[update] CUST_0002 full_name 수정 → {n}행 변경")
    conn.close()

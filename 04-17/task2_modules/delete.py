"""실습과제 2 — delete 모듈: D (Delete)."""

from __future__ import annotations

import sqlite3

from init import connect


def delete_by_username(conn: sqlite3.Connection, username: str) -> int:
    """username이 일치하는 고객 삭제. 반환: 삭제된 행 수."""
    cur = conn.execute(
        "DELETE FROM customers WHERE username = ?",
        (username,),
    )
    conn.commit()
    return cur.rowcount


if __name__ == "__main__":
    conn = connect()
    n = delete_by_username(conn, "CUST_0003")
    print(f"[delete] CUST_0003 삭제 → {n}행 제거")
    conn.close()

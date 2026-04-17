"""
06주차 실습과제 1 — customers.csv → SQLite3 CRUD Gradio 앱

원본 과제 (04_sqlite3_introduction.ipynb, 실습과제 1):
  github.com/ancestor9/data/blob/main/customers.csv 를 읽어와서
  데이터베이스를 만들고 user 테이블에 CRUD하는 코드를 만들어라.

이 앱의 구성:
  1) DB 초기화 탭 — CSV 로드 + 상위 N개 삽입
  2) Read 탭    — 전체 조회 / username 검색
  3) Create 탭  — 새 고객 추가
  4) Update 탭  — username 기준 full_name 수정
  5) Delete 탭  — username 기준 삭제

스레드 안전을 위해 연결은 함수 호출마다 새로 연다.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import gradio as gr
import pandas as pd

# ─────────────────────────── 설정 ───────────────────────────
APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "customer_data.db"
CSV_URL = "https://raw.githubusercontent.com/ancestor9/data/main/customers.csv"
DEFAULT_LIMIT = 10


# ─────────────────────────── DB 헬퍼 ───────────────────────────
def connect() -> sqlite3.Connection:
    """매 호출마다 새 연결. Gradio 멀티스레드 환경에서 안전."""
    return sqlite3.connect(DB_PATH)


def table_to_df() -> pd.DataFrame:
    """customers 테이블 전체를 DataFrame으로 반환. 테이블이 없으면 빈 DF."""
    if not DB_PATH.exists():
        return pd.DataFrame(columns=["id", "username", "full_name"])
    with connect() as conn:
        try:
            return pd.read_sql_query(
                "SELECT id, username, full_name FROM customers ORDER BY id ASC",
                conn,
            )
        except pd.errors.DatabaseError:
            return pd.DataFrame(columns=["id", "username", "full_name"])


# ─────────────────────────── 기능: 초기화 & 적재 ───────────────────────────
def init_and_load(csv_url: str, limit: int) -> tuple[str, pd.DataFrame]:
    """DB 파일을 재생성하고, CSV 상위 limit개를 customers 테이블에 삽입."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE customers (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT NOT NULL UNIQUE,
                full_name TEXT
            )
            """
        )
        conn.commit()

        try:
            df = pd.read_csv(csv_url)
        except Exception as e:
            return f"[ERROR] CSV 로드 실패: {e}", table_to_df()

        df_top = df.head(int(limit))

        # 강의 예제와 동일하게 '고객ID'를 username/full_name으로 사용
        if "고객ID" not in df.columns:
            return (
                f"[ERROR] CSV에 '고객ID' 컬럼이 없습니다. "
                f"실제 컬럼: {list(df.columns)}",
                table_to_df(),
            )
        rows = [(str(v), str(v)) for v in df_top["고객ID"].tolist()]

        cur.executemany(
            "INSERT OR IGNORE INTO customers (username, full_name) VALUES (?, ?)",
            rows,
        )
        conn.commit()
        inserted = cur.rowcount if cur.rowcount >= 0 else len(rows)

    return (
        f"[OK] 테이블 재생성 완료. {inserted}/{len(rows)}개 삽입됨.",
        table_to_df(),
    )


# ─────────────────────────── 기능: Read ───────────────────────────
def read_all() -> pd.DataFrame:
    return table_to_df()


def read_by_username(username: str) -> tuple[str, pd.DataFrame]:
    username = (username or "").strip()
    if not username:
        return "[WARN] username을 입력하세요.", table_to_df()
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, full_name FROM customers WHERE username = ?",
            (username,),
        )
        row = cur.fetchone()
    if row is None:
        return f"[INFO] '{username}' 고객 없음.", table_to_df()
    return f"[OK] 조회 결과: id={row[0]}, username={row[1]}, full_name={row[2]}", table_to_df()


# ─────────────────────────── 기능: Create ───────────────────────────
def create_customer(username: str, full_name: str) -> tuple[str, pd.DataFrame]:
    username = (username or "").strip()
    full_name = (full_name or "").strip()
    if not username:
        return "[WARN] username은 필수입니다.", table_to_df()
    if not DB_PATH.exists():
        return "[WARN] 먼저 '초기화 & 적재' 탭에서 DB를 준비하세요.", table_to_df()
    try:
        with connect() as conn:
            conn.execute(
                "INSERT INTO customers (username, full_name) VALUES (?, ?)",
                (username, full_name),
            )
            conn.commit()
    except sqlite3.IntegrityError as e:
        return f"[ERROR] 삽입 실패(UNIQUE 충돌 가능): {e}", table_to_df()
    return f"[OK] '{username}' 추가 완료.", table_to_df()


# ─────────────────────────── 기능: Update ───────────────────────────
def update_customer(username: str, new_full_name: str) -> tuple[str, pd.DataFrame]:
    username = (username or "").strip()
    if not username:
        return "[WARN] username은 필수입니다.", table_to_df()
    if not DB_PATH.exists():
        return "[WARN] 먼저 '초기화 & 적재' 탭에서 DB를 준비하세요.", table_to_df()
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE customers SET full_name = ? WHERE username = ?",
            (new_full_name, username),
        )
        conn.commit()
        changed = cur.rowcount
    if changed == 0:
        return f"[INFO] '{username}' 고객이 없어 수정된 행이 없습니다.", table_to_df()
    return f"[OK] '{username}'의 full_name 수정 완료 ({changed}행).", table_to_df()


# ─────────────────────────── 기능: Delete ───────────────────────────
def delete_customer(username: str) -> tuple[str, pd.DataFrame]:
    username = (username or "").strip()
    if not username:
        return "[WARN] username은 필수입니다.", table_to_df()
    if not DB_PATH.exists():
        return "[WARN] 먼저 '초기화 & 적재' 탭에서 DB를 준비하세요.", table_to_df()
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE username = ?", (username,))
        conn.commit()
        deleted = cur.rowcount
    if deleted == 0:
        return f"[INFO] '{username}' 고객 없음. 삭제된 행 0.", table_to_df()
    return f"[OK] '{username}' 삭제 완료 ({deleted}행).", table_to_df()


# ─────────────────────────── Gradio UI ───────────────────────────
def build_ui() -> gr.Blocks:
    with gr.Blocks(title="06주차 실습과제 1 — Customers CRUD") as demo:
        gr.Markdown(
            """
            # 06주차 실습과제 1 — Customers SQLite CRUD

            `customers.csv`를 불러와 **SQLite3 DB**의 `customers` 테이블에
            Create / Read / Update / Delete를 수행합니다.

            > 사용 순서: ① **초기화 & 적재** → ② Read/Create/Update/Delete 탭
            """
        )

        with gr.Tab("① 초기화 & 적재"):
            csv_in = gr.Textbox(label="CSV URL", value=CSV_URL)
            limit_in = gr.Slider(
                minimum=1, maximum=100, value=DEFAULT_LIMIT, step=1, label="삽입할 상위 N개"
            )
            init_btn = gr.Button("초기화 + 상위 N개 적재", variant="primary")
            init_msg = gr.Textbox(label="결과", interactive=False)
            init_tbl = gr.DataFrame(label="customers 테이블")
            init_btn.click(
                init_and_load, inputs=[csv_in, limit_in], outputs=[init_msg, init_tbl]
            )

        with gr.Tab("② Read (조회)"):
            read_all_btn = gr.Button("전체 조회")
            read_tbl = gr.DataFrame(label="customers 테이블")
            read_all_btn.click(read_all, outputs=[read_tbl])

            gr.Markdown("---")
            read_user_in = gr.Textbox(label="username으로 검색 (예: CUST_0002)")
            read_user_btn = gr.Button("검색")
            read_user_msg = gr.Textbox(label="결과", interactive=False)
            read_user_tbl = gr.DataFrame(label="customers 테이블")
            read_user_btn.click(
                read_by_username,
                inputs=[read_user_in],
                outputs=[read_user_msg, read_user_tbl],
            )

        with gr.Tab("③ Create (추가)"):
            c_user = gr.Textbox(label="username (고유)")
            c_full = gr.Textbox(label="full_name")
            c_btn = gr.Button("추가", variant="primary")
            c_msg = gr.Textbox(label="결과", interactive=False)
            c_tbl = gr.DataFrame(label="customers 테이블")
            c_btn.click(create_customer, inputs=[c_user, c_full], outputs=[c_msg, c_tbl])

        with gr.Tab("④ Update (수정)"):
            u_user = gr.Textbox(label="대상 username (예: CUST_0002)")
            u_full = gr.Textbox(label="새 full_name")
            u_btn = gr.Button("수정", variant="primary")
            u_msg = gr.Textbox(label="결과", interactive=False)
            u_tbl = gr.DataFrame(label="customers 테이블")
            u_btn.click(update_customer, inputs=[u_user, u_full], outputs=[u_msg, u_tbl])

        with gr.Tab("⑤ Delete (삭제)"):
            d_user = gr.Textbox(label="대상 username (예: CUST_0003)")
            d_btn = gr.Button("삭제", variant="stop")
            d_msg = gr.Textbox(label="결과", interactive=False)
            d_tbl = gr.DataFrame(label="customers 테이블")
            d_btn.click(delete_customer, inputs=[d_user], outputs=[d_msg, d_tbl])

    return demo


if __name__ == "__main__":
    demo = build_ui()
    # SHARE=1 환경변수가 있으면 *.gradio.live 공개 URL 발급, 아니면 로컬만.
    # 안랩 등 보안 SW가 frpc를 오탐해 차단하는 환경에서는 SHARE=0으로 두고
    # Hugging Face Spaces 배포를 사용한다 (README 참고).
    share = os.environ.get("SHARE", "0") == "1"
    demo.launch(share=share, server_name="127.0.0.1", server_port=7860)

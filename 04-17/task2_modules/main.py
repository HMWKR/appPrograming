"""실습과제 2 — main.py
5개 모듈(init/create/read/update/delete)을 조합해 강의 Cell 13과 동일한
시연 시나리오를 순차 실행한다.

실행 방법:
    cd task2_modules
    python main.py
"""

from __future__ import annotations

import init
import create
import read
import update
import delete


def main() -> None:
    # 1) 초기화
    conn = init.init_db(fresh=True)
    print(f"[1/7] init_db 완료 → {init.DB_PATH.name}")

    # 2) CSV에서 상위 10개 적재
    n = create.load_from_csv(conn, limit=10)
    print(f"[2/7] create.load_from_csv → {n}개 시도")

    # 3) 전체 조회
    print("[3/7] read.fetch_all:")
    for row in read.fetch_all(conn):
        print("       ", row)

    # 4) 단건 조회
    target = "CUST_0002"
    print(f"[4/7] read.fetch_by_username('{target}') → {read.fetch_by_username(conn, target)}")

    # 5) 수정
    nu = update.update_full_name(conn, target, "Updated User 02")
    print(f"[5/7] update.update_full_name('{target}') → {nu}행 수정")

    # 6) 삭제
    victim = "CUST_0003"
    nd = delete.delete_by_username(conn, victim)
    print(f"[6/7] delete.delete_by_username('{victim}') → {nd}행 삭제")

    # 7) 최종 상태
    print("[7/7] 최종 read.fetch_all:")
    for row in read.fetch_all(conn):
        print("       ", row)
    print(f"       총 {read.count(conn)}행")

    conn.close()


if __name__ == "__main__":
    main()

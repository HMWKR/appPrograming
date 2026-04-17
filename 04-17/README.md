# 06주차 / 04_sqlite3_introduction.ipynb — 정리 & 실습과제 산출물

## 파일 구성

| 파일 | 설명 |
|---|---|
| `00_개념요약.md` | 노트북 전체 개념 지도 + 학습 목표 + 용어표 (CLAUDE.md 표준) |
| `01_코드해설.md` | 노트북 17개 셀의 셀 단위 해설 (CLAUDE.md 표준) |
| `02_실습과제1_정리.md` | 실습과제 1 상세 — CSV → SQLite CRUD + Gradio 설계 해설 |
| `03_실습과제2_정리.md` | 실습과제 2 상세 — 모듈 리팩토링 설계 결정 |
| `task1_gradio_app.py` | 실습과제 1 산출물 — Gradio CRUD 앱 |
| `task2_modules/` | 실습과제 2 산출물 — init/create/read/update/delete/main 6개 모듈 |
| `requirements.txt` | Gradio 배포용(HF Spaces) 의존성 |
| `customer_data.db` | 실행 시 자동 생성되는 SQLite 파일 (review/ 과 task2_modules/ 각각 생성됨) |
| `README.md` | 이 파일 |

---

## 실습과제 2 실행 (콘솔 데모)

```bash
cd "C:\Users\jusan\Desktop\2026-1학기\조상구 교수님\program\06week\week6\review\task2_modules"
python main.py
```

출력에 `[1/7] ... [7/7]` 순서로 초기화 → CSV 적재 → 전체 조회 → 단건 조회 → 수정 → 삭제 → 최종 조회가 나타납니다. 각 모듈(`init.py`, `create.py`, `read.py`, `update.py`, `delete.py`)을 **단독 실행**할 수도 있습니다.

---

## 실습과제 1 — 로컬 실행 (기본)

```bash
cd "C:\Users\jusan\Desktop\2026-1학기\조상구 교수님\program\06week\week6\review"
python task1_gradio_app.py
```

정상 실행 시 출력:
```
* Running on local URL:  http://127.0.0.1:7860
```
브라우저에서 `http://127.0.0.1:7860` 으로 접속.

## 공개 URL(*.gradio.live) 발급 — 선택

```bash
# Windows CMD
set SHARE=1 && python task1_gradio_app.py
# PowerShell
$env:SHARE=1; python task1_gradio_app.py
```

출력에 `Running on public URL: https://xxxxxxxxxxxx.gradio.live` 추가됨 (72시간 유효).

### ⚠ 안랩(AhnLab Safe Transaction) 오탐 주의

본 PC에서 `SHARE=1` 실행 시 안랩이 `C:\Users\jusan\.cache\huggingface\gradio\frpc\frpc_windows_amd64_*.exe`를 **`HackTool/Win.Frpc`** 로 탐지하여 차단할 수 있다. 이는 **오탐**이며 `frpc`는 Hugging Face가 서명·배포하는 합법 터널링 바이너리이다.

해결:
1. 안랩 팝업에서 **[닫기]** 선택 (치료 X — 치료하면 파일 삭제됨).
2. 안랩 설정 → **예외(허용) 목록에 경로 추가**:
   `C:\Users\jusan\.cache\huggingface\gradio\frpc\`
3. 앱을 `set SHARE=1` 로 재실행.

예외 등록이 회사/기관 정책상 불가하면 아래 **Hugging Face Spaces 배포**를 권장.

---

## 사용 순서

1. **탭 ① 초기화 & 적재** → `초기화 + 상위 N개 적재` 버튼 클릭.
   - CSV URL 기본값은 강의 과제의 `customers.csv` raw URL.
   - 슬라이더로 1~100개 조정 가능. 기본 10.
2. **탭 ② Read** → `전체 조회` 또는 `CUST_0002` 등 검색.
3. **탭 ③ Create** → 신규 고객 추가 (예: `CUST_TEST`, `Test User`).
4. **탭 ④ Update** → `CUST_0002` 의 full_name 변경.
5. **탭 ⑤ Delete** → `CUST_0003` 삭제.

각 탭 하단의 `customers 테이블` DataFrame이 조작 직후 자동 갱신됩니다.

---

## 의존성

- `gradio >= 5.0` (확인: 6.9.0)
- `pandas >= 2.0` (확인: 2.2.3)
- `sqlite3` (Python 표준 라이브러리)

설치되어 있지 않다면:
```bash
pip install gradio pandas
```

---

## 공개 URL이 생성되지 않을 때

- 회사/학교 방화벽이 `*.gradio.live` 터널을 차단할 수 있음.
- 그럴 때는 `demo.launch(share=False)` 로 돌려 로컬 접속만 이용하거나, Hugging Face Spaces에 업로드.

### Hugging Face Spaces 상시 배포 (권장 대안)

공개 URL이 필요하고 `*.gradio.live` 방법이 막혀있을 때 가장 확실한 경로.

1. https://huggingface.co 가입 → 우측 상단 **New** → **Space**.
2. 설정:
   - Space name: `customer-crud-demo` (원하는 이름)
   - Space SDK: **Gradio**
   - License: 원하는 라이선스
3. 생성된 Space 저장소에 3개 파일 업로드:
   - `task1_gradio_app.py` → **`app.py`** 로 파일명 변경 (HF Spaces 관례)
   - `requirements.txt` (이미 본 폴더에 준비됨)
   - (선택) `README.md`
4. 업로드 후 자동 빌드 → 1~2분 후
   `https://huggingface.co/spaces/<username>/customer-crud-demo` 에서 상시 접속.

**주의**: HF Spaces는 컨테이너 재시작 시 DB 파일이 초기화된다 (ephemeral FS). 이 앱은 "① 초기화 & 적재" 버튼으로 언제든 재적재할 수 있어 무리 없음.

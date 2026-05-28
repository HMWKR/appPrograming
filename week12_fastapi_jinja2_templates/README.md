# 12주차 FastAPI Jinja2 프로젝트

- 이름: 이성민
- 학과: 소프트웨어융합과
- 학년: 2학년
- 학번: 2151050

## 구성

| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI 라우팅과 템플릿 컨텍스트 구성 |
| `templates/base.html` | 공통 HTML 레이아웃 |
| `templates/playlist.html` | 플레이리스트 목록 페이지 |
| `templates/piece.html` | 곡 상세 페이지 |
| `static/style.css` | 화면 스타일 |
| `static/script.js` | 브라우저 상호작용 |

## 실행

```bash
uvicorn main:app --reload
```

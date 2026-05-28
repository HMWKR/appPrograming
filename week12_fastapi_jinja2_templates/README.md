# 12주차 FastAPI Jinja2 템플릿

- 이름: 이성민
- 학과: 소프트웨어융합과
- 학년: 2학년
- 학번: 2151050

## 학습 내용

FastAPI에서 HTML 페이지를 반환하고, Jinja2 템플릿과 정적 파일을 분리하는 구조를 정리한 과제입니다.  
Python은 라우팅과 데이터 준비를 담당하고, HTML/CSS/JavaScript는 화면 구성을 담당하도록 분리했습니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `week12_fastapi_jinja2_templates_explained.ipynb` | HTML 반환 방식과 템플릿 분리 과정을 설명한 노트북 |
| `main.py` | FastAPI 라우팅과 템플릿 컨텍스트 구성 |
| `templates/base.html` | 공통 레이아웃 |
| `templates/playlist.html` | 플레이리스트 목록 화면 |
| `templates/piece.html` | 곡 상세 화면 |
| `static/style.css` | 화면 스타일 |
| `static/script.js` | 브라우저 상호작용 |

## 실행

```bash
uvicorn main:app --reload
```

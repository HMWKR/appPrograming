# 앱프로그래밍 시트 기준 과제 재구성

- 이름: 이성민
- 학과: 소프트웨어융합과
- 학년: 2학년
- 학번: 2151050

## 과제 매핑

| 순서 | 시트 열 | 디렉토리 | 노트북 |
|---:|---|---|---|
| 1 | 0313_HomeWork | `week01_0313_rocket_titanic_etl` | `week01_0313_rocket_titanic_etl_explained.ipynb` |
| 2 | 0320_HomeWork(과제1) | `week02_0320_blood_donation_eda` | `week02_0320_blood_donation_eda_explained.ipynb` |
| 3 | Tom and Jerry Show | `week03_0320_tom_jerry_oop` | `week03_0320_tom_jerry_oop_explained.ipynb` |
| 4 | 0327_TASK2 HomeWork | `week04_0327_rest_dataframe_gradio` | `week04_0327_rest_dataframe_gradio_explained.ipynb` |
| 5 | 0403_Self HomeWork scrapping books | `week05_0403_static_scraping_books` | `week05_0403_static_scraping_books_explained.ipynb` |
| 6 | 0410 webtoon | `week06_0410_webtoon_scraping` | `week06_0410_webtoon_scraping_explained.ipynb` |
| 7 | 417_DB-CRUD-gradio 서비스(점수반영) Quiz-Test | `week07_0417_sqlite_crud_validation` | `week07_0417_sqlite_crud_validation_explained.ipynb` |
| 8 | FAST API 사이트 실습코드(4-29) | `week08_0429_fastapi_practice` | `week08_0429_fastapi_practice_explained.ipynb` |
| 9 | FastAPI 검증 모델 | `week09_fastapi_validation_models` | `week09_annotated_query_model_explained.ipynb` |
| 10 | 머신러닝 웹서비스 | `week10_ml_web_service` | `week10_ml_fastapi_gradio_service_explained.ipynb` |
| 11 | 와인 분류 대시보드 | `week11_wine_dashboard_service` | `week11_wine_dashboard_service_explained.ipynb` |
| 12 | FastAPI와 Jinja2 템플릿 | `week12_fastapi_jinja2_templates` | `week12_fastapi_jinja2_templates_explained.ipynb` |

## 작성 및 검증 흐름

1. 과제 시트의 열 이름을 기준으로 제출 대상 주차를 정리했습니다.
2. 1~8주차는 기존 제출 흐름을 유지하고, 9~12주차는 주제별 디렉토리와 설명 노트북을 추가했습니다.
3. 각 노트북은 실행 가능한 코드 셀과 코드 의도를 설명하는 마크다운 셀로 구성했습니다.
4. 보조 실행 파일이 필요한 주차는 `README.md`와 Python 파일을 포함했습니다.
5. 전체 노트북을 `jupyter nbconvert --execute --inplace`로 실행해 오류 여부를 확인했습니다.
6. 노트북 내부 error output, 외부 URL 문자열, 불필요한 생성 파일 포함 여부를 추가로 검사했습니다.

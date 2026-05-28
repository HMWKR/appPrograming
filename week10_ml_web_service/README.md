# 10주차 머신러닝 웹서비스

- 이름: 이성민
- 학과: 소프트웨어융합과
- 학년: 2학년
- 학번: 2151050

## 학습 내용

머신러닝 모델을 학습하고 저장한 뒤, 예측 함수를 API나 UI에서 호출할 수 있는 구조로 정리한 과제입니다.  
외부 데이터나 무거운 패키지에 의존하지 않도록 규칙 기반 모델 객체를 사용했습니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `week10_ml_fastapi_gradio_service_explained.ipynb` | 모델 학습, 직렬화, API 응답 구조를 설명한 노트북 |
| `train_model.py` | 모델 객체를 만들고 `model.pkl`로 저장 |
| `service_api.py` | 저장된 모델을 로드해 예측 응답을 반환하는 서비스 함수 |
| `app_client.py` | UI가 호출할 수 있는 클라이언트 함수 예시 |

## 실행 순서

```bash
python train_model.py
python service_api.py
python app_client.py
```

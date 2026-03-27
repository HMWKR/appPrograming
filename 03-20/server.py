# ============================================================
# 과제 3: HTTP Server — FastAPI + Uvicorn 기반 로컬 HTTP 서버
# ============================================================
# 실행: python server.py  (또는 uvicorn server:app --port 8080)
# 종료: Ctrl+C
# ============================================================
#
# ── 컴퓨터 과학 배경 ──
#
# HTTP(HyperText Transfer Protocol)는 OSI 7계층 모델에서
# **응용 계층(Application Layer)**에 해당하는 프로토콜이다.
#
#   [7] 응용 계층    ← HTTP 요청/응답이 여기서 동작
#   [6] 표현 계층    ← JSON 직렬화/역직렬화 (데이터 포맷 변환)
#   [5] 세션 계층    ← HTTP 커넥션 관리
#   [4] 전송 계층    ← TCP 소켓 (포트 번호, 신뢰성 보장)
#   [3] 네트워크 계층 ← IP 주소 (localhost = 127.0.0.1)
#   [2] 데이터링크 계층
#   [1] 물리 계층
#
# 클라이언트가 서버에 요청을 보내면, 이 7계층을 위→아래로 내려가
# 네트워크를 거쳐 서버에 도달하고, 서버는 아래→위로 올라가며
# 요청을 해석한다. 응답도 같은 과정을 역방향으로 거친다.
#
# HTTP의 핵심 특징:
# - **무상태(Stateless)**: 각 요청은 독립적. 이전 요청을 기억하지 않음.
#   → 서버 확장(Scale-out)에 유리하지만, 세션 유지가 필요하면 쿠키/토큰 필요.
# - **요청-응답(Request-Response)** 모델: 항상 클라이언트가 먼저 요청.
#   → 서버는 자발적으로 클라이언트에게 데이터를 보낼 수 없음(WebSocket은 별도).
#
# ── WSGI vs ASGI ──
#
# 전통적 Python 웹 서버는 WSGI(Web Server Gateway Interface)를 사용했다.
# WSGI는 **동기(Synchronous)** 방식으로, 요청 하나를 처리하는 동안
# 다른 요청은 대기해야 했다.
#
# ASGI(Asynchronous Server Gateway Interface)는 이를 개선한 비동기 표준이다.
# - **비동기(Async)**: 한 요청의 I/O 대기 중에 다른 요청을 처리할 수 있음
# - **이벤트 루프**: asyncio 기반으로 동시성(Concurrency)을 달성
# - uvicorn은 ASGI 서버, FastAPI는 ASGI 프레임워크
#
# 비유: WSGI = 은행 창구 1개 (한 명씩 처리)
#       ASGI = 은행 창구 1개 + 대기 호출 시스템 (서류 준비하는 동안 다음 고객 처리)
#
# ============================================================

# --- 라이브러리 임포트 ---

from fastapi import FastAPI, Request
# FastAPI: ASGI 기반 웹 프레임워크.
#   내부적으로 Starlette(비동기 웹 프레임워크) 위에 구축되어 있다.
#   @app.get(), @app.post() 같은 데코레이터로 URL 경로와 함수를 연결(라우팅)한다.
#
# Request: HTTP 요청 객체. 클라이언트가 보낸 헤더, 본문, 쿼리 파라미터 등을 담고 있다.
#   네트워크 관점: TCP 소켓으로 수신된 바이트 스트림을 파싱(parsing)한 결과물.

from fastapi.responses import JSONResponse
# JSONResponse: HTTP 응답을 JSON 형식으로 반환하는 클래스.
#   내부 동작:
#     1. Python dict → json.dumps()로 JSON 문자열 변환 (직렬화, Serialization)
#     2. 문자열 → UTF-8 바이트로 인코딩
#     3. Content-Type: application/json 헤더 자동 설정
#   왜 JSON인가? HTTP 자체는 텍스트 프로토콜이라 바이너리 객체를 직접 보낼 수 없다.
#   JSON은 사람이 읽을 수 있고, 언어에 독립적인 텍스트 직렬화 포맷이기 때문.

import uvicorn
# uvicorn: ASGI 서버 구현체. 실제로 TCP 소켓을 열고 HTTP 요청을 수신하는 역할.
#   OS 수준에서 일어나는 일:
#     1. socket() 시스템콜로 TCP 소켓 생성
#     2. bind()로 (HOST, PORT) 주소에 소켓을 바인딩
#     3. listen()으로 커넥션 대기열(backlog) 설정
#     4. accept()로 클라이언트 연결 수락 → 새 소켓 생성
#     5. recv()/send()로 데이터 송수신
#   이 모든 과정을 uvicorn이 내부적으로 처리해준다.


# --- FastAPI 앱 생성 ---

app = FastAPI()
# FastAPI() 인스턴스가 생성되면:
#   1. 라우팅 테이블(URL → 함수 매핑) 초기화
#   2. 미들웨어 체인 구성 (요청 전처리 → 핸들러 → 응답 후처리)
#   3. ASGI 인터페이스 준비 (uvicorn이 이 app 객체의 __call__을 호출)
#
# 디자인 패턴: **ASGI Application 패턴**
#   uvicorn(서버)이 app(애플리케이션)을 호출하는 구조.
#   서버와 애플리케이션의 관심사가 분리(Separation of Concerns)된다.
#   → 서버는 네트워크 처리에 집중, 앱은 비즈니스 로직에 집중.


# --- GET 엔드포인트: "/" ---

@app.get("/")
# 데코레이터(Decorator) 패턴:
#   @app.get("/")은 아래 함수를 FastAPI의 라우팅 테이블에 등록한다.
#   HTTP GET 메서드 + "/" 경로로 요청이 들어오면 이 함수가 실행된다.
#
#   HTTP 메서드란?
#   - GET:    리소스 조회 (읽기). 본문(body) 없음. 멱등(Idempotent).
#   - POST:   리소스 생성 (쓰기). 본문에 데이터 포함. 비멱등.
#   - PUT:    리소스 전체 교체. DELETE: 리소스 삭제.
#   "멱등"이란 같은 요청을 여러 번 보내도 결과가 동일하다는 뜻.
#   GET /는 몇 번을 호출해도 같은 응답 → 안전한 조회 작업.
async def root():
    # async def: 비동기 함수(코루틴, Coroutine) 선언.
    #   파이썬의 asyncio 이벤트 루프 위에서 실행된다.
    #   이벤트 루프란? 단일 스레드에서 여러 비동기 작업을 번갈아 실행하는 구조.
    #
    #   왜 비동기인가?
    #   웹 서버의 대부분의 시간은 "대기"이다 (네트워크 I/O, DB 쿼리 응답 대기 등).
    #   동기 방식은 대기 중 아무것도 못 하지만, 비동기는 대기 중 다른 요청을 처리.
    #   → 단일 프로세스로도 수천 개의 동시 연결을 처리할 수 있다.

    response = {
        "message": "안녕하세요! 머신러닝(2) HTTP 서버입니다.",
        "method": "GET",
        "path": "/",
    }
    # Python dict → FastAPI가 자동으로 JSON 직렬화 → HTTP 응답 본문(body)이 된다.
    #
    # HTTP 응답 구조 (실제 네트워크로 전송되는 텍스트):
    #   HTTP/1.1 200 OK\r\n              ← 상태 라인 (프로토콜 버전 + 상태 코드)
    #   content-type: application/json\r\n ← 헤더 (메타데이터)
    #   \r\n                               ← 빈 줄 (헤더와 본문 구분)
    #   {"message": "안녕하세요!..."}      ← 본문 (실제 데이터)
    #
    # 상태 코드 200은 "성공"을 의미한다.
    #   2xx = 성공, 3xx = 리다이렉트, 4xx = 클라이언트 오류, 5xx = 서버 오류.
    return response


# --- POST 엔드포인트: "/data" ---

@app.post("/data")
# POST /data: 클라이언트가 서버에 데이터를 "보내는" 요청.
#   GET과의 핵심 차이: POST는 요청 본문(body)에 데이터를 포함할 수 있다.
#   URL에 데이터를 노출하지 않으므로 GET보다 보안적으로 유리하다.
async def receive_data(request: Request):
    # Request 객체: uvicorn이 TCP 소켓에서 읽은 원시 바이트를
    #   HTTP 프로토콜에 따라 파싱한 결과이다.
    #
    #   TCP 소켓에서 수신된 원시 데이터 예시:
    #     POST /data HTTP/1.1\r\n
    #     Host: localhost:8080\r\n
    #     Content-Type: application/json\r\n
    #     Content-Length: 95\r\n
    #     \r\n
    #     {"student": "홍길동", "subject": "머신러닝(2)"}
    #
    #   uvicorn이 이것을 파싱하여:
    #     request.method = "POST"
    #     request.url.path = "/data"
    #     request.headers = {"content-type": "application/json", ...}
    #     request.body() = b'{"student": "홍길동", ...}'
    #   로 구조화해준다.

    # --- 요청 본문(body) 읽기 ---
    body = await request.body()
    # await: 비동기 I/O 대기. TCP 소켓에서 바이트를 읽는 동안
    #   이벤트 루프는 다른 요청을 처리할 수 있다.
    #
    # request.body()가 반환하는 것: bytes 타입의 원시 바이트열.
    #   네트워크로 전송되는 모든 데이터는 바이트(0과 1)이다.
    #   텍스트는 인코딩(UTF-8 등) 규칙에 따라 바이트로 변환된 것일 뿐이다.

    # --- JSON 역직렬화(Deserialization) ---
    try:
        data = await request.json()
        # request.json() 내부 동작:
        #   1. body 바이트를 UTF-8로 디코딩 → 문자열
        #      b'{"student": "\xed\x99\x8d..."}' → '{"student": "홍길동"...}'
        #   2. json.loads()로 JSON 문자열 → Python dict 변환
        #      '{"student": "홍길동"}' → {"student": "홍길동"}
        #
        # 이것이 "역직렬화(Deserialization)"이다.
        # 직렬화(Serialization): Python 객체 → 전송 가능한 형식(JSON 문자열/바이트)
        # 역직렬화: 전송된 형식 → Python 객체
        # 왜 필요한가? 네트워크는 바이트만 전송할 수 있고, Python dict는 메모리상 객체이므로
        # 양쪽을 변환하는 과정이 반드시 필요하다.
    except Exception:
        data = {"raw": body.decode("utf-8")}
        # JSON 파싱 실패 시: 원본 텍스트를 그대로 저장.
        # 방어적 프로그래밍(Defensive Programming): 예상치 못한 입력에도 서버가 죽지 않도록.

    response = {
        "message": "데이터를 성공적으로 수신했습니다.",
        "method": "POST",
        "received_data": data,
    }

    return JSONResponse(content=response, status_code=200)
    # JSONResponse: dict → JSON 바이트로 직렬화하여 HTTP 응답을 구성한다.
    #   status_code=200: "OK" — 요청이 성공적으로 처리되었음을 클라이언트에게 알린다.


# --- 서버 실행 ---

if __name__ == "__main__":
    # __name__ == "__main__":
    #   이 조건은 "이 파일이 직접 실행될 때만" 아래 코드를 실행한다.
    #   다른 파일에서 import할 때는 실행되지 않는다.
    #   왜? 모듈 재사용성 — app 객체만 import하여 테스트하거나 다른 서버에 연결할 수 있다.

    HOST = "127.0.0.1"
    # 127.0.0.1 (= localhost): 루프백(Loopback) 주소.
    #   OS의 네트워크 스택 내부에서만 순환하는 가상 주소이다.
    #   실제 네트워크 카드(NIC)를 거치지 않으므로 외부에서 접근 불가.
    #   개발/테스트 환경에서 자기 자신에게만 서비스할 때 사용한다.
    #   "0.0.0.0"으로 바꾸면 모든 네트워크 인터페이스에서 접속 가능 (보안 주의).

    PORT = 8080
    # 포트(Port): TCP에서 하나의 IP 주소 내에서 여러 서비스를 구분하는 번호.
    #   0~1023: Well-known 포트 (80=HTTP, 443=HTTPS, 22=SSH) — 관리자 권한 필요.
    #   1024~49151: 등록 포트 — 일반 사용자가 사용 가능. 8080은 HTTP 대체 포트로 관례적 사용.
    #   49152~65535: 동적/임시 포트 — OS가 클라이언트에 자동 할당.
    #
    # 서버 시작 시 OS 수준에서 일어나는 일:
    #   1. socket(AF_INET, SOCK_STREAM) → TCP 소켓 생성
    #      AF_INET = IPv4 주소 체계, SOCK_STREAM = TCP (연결 지향, 신뢰성 보장)
    #   2. bind(("127.0.0.1", 8080)) → 이 소켓을 특정 주소:포트에 할당
    #   3. listen(backlog) → 연결 대기열 크기 설정
    #   4. 이벤트 루프 시작 → accept()로 클라이언트 연결을 비동기적으로 수락

    print(f"서버가 http://{HOST}:{PORT} 에서 실행 중입니다...")
    print("종료하려면 Ctrl+C를 누르세요.\n")

    uvicorn.run(app, host=HOST, port=PORT)
    # uvicorn.run()이 하는 일:
    #   1. asyncio 이벤트 루프 생성
    #   2. TCP 소켓 바인딩 (위에서 설명한 socket→bind→listen)
    #   3. 이벤트 루프에서 무한 대기:
    #      - 새 TCP 연결 감지 → accept()
    #      - 수신 데이터 감지 → HTTP 파싱 → app.__call__() 호출
    #      - 응답 준비 완료 → send()로 클라이언트에게 전송
    #   4. Ctrl+C(SIGINT 시그널) 수신 → graceful shutdown (연결 정리 후 종료)
    #
    # 전체 요청-응답 흐름 요약:
    #   Client                          Server (uvicorn + FastAPI)
    #     │                                │
    #     │ ── TCP 3-way handshake ──────→ │  (SYN → SYN-ACK → ACK)
    #     │ ── HTTP 요청 전송 ───────────→ │  (GET / HTTP/1.1...)
    #     │                                │  → uvicorn이 HTTP 파싱
    #     │                                │  → FastAPI 라우팅 테이블에서 핸들러 찾기
    #     │                                │  → async def root() 실행
    #     │                                │  → dict → JSON 직렬화
    #     │ ←── HTTP 응답 전송 ─────────── │  (HTTP/1.1 200 OK...)
    #     │ ── TCP 연결 종료 ────────────→ │  (FIN → ACK)

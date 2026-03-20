# ============================================================
# 과제 3: HTTP Client — 서버에 GET/POST 요청 전송
# ============================================================
# 사전 조건: 다른 터미널에서 server.py가 실행 중이어야 합니다.
# 실행: python client.py
# ============================================================
#
# ── 컴퓨터 과학 배경: 클라이언트-서버 모델 ──
#
# 클라이언트-서버(Client-Server)는 네트워크 통신의 가장 기본적인 아키텍처이다.
#
#   클라이언트(Client): 서비스를 "요청"하는 쪽.
#     → 웹 브라우저, 모바일 앱, 이 스크립트(client.py)가 클라이언트이다.
#   서버(Server): 서비스를 "제공"하는 쪽.
#     → server.py가 서버이다. 항상 켜져 있으며, 요청을 기다린다.
#
# 이 모델의 핵심 제약:
#   - 클라이언트가 "먼저" 요청해야 통신이 시작된다.
#   - 서버는 자발적으로 클라이언트에게 데이터를 보낼 수 없다.
#   - 1개의 서버에 N개의 클라이언트가 동시에 접속할 수 있다(1:N 관계).
#
# ── 왜 urllib인가? ──
#
# urllib.request는 Python 표준 라이브러리이므로 추가 설치 없이 사용 가능하다.
# 내부적으로 OS의 소켓 API를 직접 호출하여 TCP 연결을 생성한다.
# 더 편리한 라이브러리(requests, httpx)도 있지만, 표준 라이브러리만으로
# HTTP 통신의 원리를 이해하는 것이 학습 목적에 더 적합하다.
#
# ============================================================

# --- 라이브러리 임포트 ---

import urllib.request
# urllib.request: Python 표준 라이브러리의 HTTP 클라이언트 모듈.
#   내부적으로 다음 과정을 수행한다:
#     1. socket.create_connection()으로 TCP 소켓 생성 + 서버에 연결
#     2. HTTP 요청 텍스트를 조립 (메서드, 헤더, 본문)
#     3. 소켓의 send()로 요청 바이트 전송
#     4. 소켓의 recv()로 응답 바이트 수신
#     5. HTTP 응답을 파싱하여 상태 코드, 헤더, 본문 분리

import json
# json: 직렬화(Serialization) / 역직렬화(Deserialization) 모듈.
#   json.dumps(): Python dict → JSON 문자열 (직렬화)
#   json.loads(): JSON 문자열 → Python dict (역직렬화)
#
#   왜 JSON을 쓰는가?
#   - 사람이 읽을 수 있는(Human-readable) 텍스트 형식
#   - 언어에 독립적(Language-agnostic): Python, JS, Java 모두 파싱 가능
#   - HTTP의 Content-Type: application/json으로 표준화되어 있음
#   - 대안: XML(무겁고 장황), Protocol Buffers(빠르지만 사람이 읽기 어려움)


# --- 서버 주소 설정 ---

SERVER_URL = "http://localhost:8080"
# URL(Uniform Resource Locator)의 구조:
#   http://    localhost    :8080     /path
#   ──────    ──────────    ─────    ──────
#   프로토콜    호스트명      포트     경로
#
# - http://: 스킴(Scheme). 어떤 프로토콜을 사용할지 지정.
#     http = 평문 전송, https = TLS/SSL 암호화 전송.
# - localhost: 호스트명. DNS가 이것을 IP 주소 127.0.0.1로 변환(resolve)한다.
#     DNS(Domain Name System)는 사람이 읽는 이름 → IP 주소 변환 서비스.
#     localhost는 특별한 주소로, OS의 hosts 파일에서 바로 127.0.0.1로 매핑된다.
# - :8080: 포트 번호. 생략하면 http의 기본 포트 80이 사용된다.
# - /path: 서버 내에서 어떤 리소스(엔드포인트)에 접근할지 지정.


# --- GET 요청 함수 ---

def send_get():
    """
    GET 요청을 서버에 보내고 응답을 출력한다.

    GET 요청은 HTTP에서 가장 기본적인 메서드이다.
    "서버야, 이 경로(/)에 있는 데이터를 보여줘"라는 의미.
    본문(body)을 포함하지 않으며, 멱등(Idempotent)하다.
    → 같은 GET 요청을 100번 보내도 서버 상태가 변하지 않는다.
    """
    print("=" * 60)
    print("[1] GET 요청 전송")
    print("=" * 60)

    # --- 1단계: Request 객체 생성 ---
    req = urllib.request.Request(f"{SERVER_URL}/")
    # Request 객체는 아직 네트워크 연결을 만들지 않는다.
    # HTTP 요청의 "설계도"만 만드는 단계이다.
    # 기본값: method="GET", headers는 User-Agent 등 최소 헤더만 포함.
    #
    # 이 객체가 담고 있는 정보:
    #   - URL: http://localhost:8080/
    #   - Method: GET
    #   - Headers: {"User-Agent": "Python-urllib/3.x"}

    # --- 2단계: 요청 전송 + 응답 수신 ---
    with urllib.request.urlopen(req) as res:
        # urlopen()이 호출되는 순간, 실제 네트워크 통신이 시작된다.
        #
        # OS/네트워크 수준에서 일어나는 일 (TCP/IP 4계층):
        #
        # [1] DNS 해석 (응용 계층)
        #     "localhost" → 127.0.0.1 변환.
        #     localhost는 OS의 hosts 파일에서 직접 해석되므로 DNS 서버 조회 없음.
        #
        # [2] TCP 3-way Handshake (전송 계층)
        #     클라이언트 → 서버: SYN (연결 요청)
        #     서버 → 클라이언트: SYN-ACK (요청 수락)
        #     클라이언트 → 서버: ACK (확인)
        #     → 이 3단계가 완료되어야 TCP 연결이 "수립(Established)"된다.
        #     왜 3번인가? 양쪽 모두 송수신 능력을 확인해야 하므로.
        #
        # [3] HTTP 요청 전송 (응용 계층)
        #     실제로 소켓에 쓰이는 텍스트:
        #       GET / HTTP/1.1\r\n
        #       Host: localhost:8080\r\n
        #       User-Agent: Python-urllib/3.x\r\n
        #       \r\n
        #     \r\n(CRLF)은 HTTP에서 "헤더 끝"을 의미하는 구분자.
        #     GET에는 본문이 없으므로 헤더 뒤에 바로 종료.
        #
        # [4] HTTP 응답 수신
        #     서버가 처리 후 응답을 보낸다:
        #       HTTP/1.1 200 OK\r\n
        #       content-type: application/json\r\n
        #       \r\n
        #       {"message": "안녕하세요!..."}
        #
        # with 문(Context Manager): 응답 처리가 끝나면 자동으로 연결을 닫는다.
        #   내부적으로 res.close()가 호출되어 TCP 소켓이 정리된다.
        #   → 리소스 누수(Resource Leak) 방지. 소켓은 OS의 한정된 자원이다.

        body = res.read().decode("utf-8")
        # res.read(): 응답 본문의 바이트(bytes)를 읽는다.
        #   네트워크로 수신된 원시 데이터: b'{"message": "\xec\x95\x88..."}'
        # .decode("utf-8"): 바이트 → 문자열 변환.
        #   UTF-8은 유니코드 문자를 1~4바이트로 인코딩하는 가변 길이 인코딩.
        #   한글 "안"은 UTF-8로 3바이트: \xec\x95\x88
        #   영문 "A"는 1바이트: \x41
        #   왜 UTF-8인가? 전 세계 모든 문자를 표현하면서도 ASCII와 호환되기 때문.

        data = json.loads(body)
        # JSON 문자열 → Python dict 역직렬화.
        #   '{"message": "안녕하세요"}' → {"message": "안녕하세요"}
        #   JSON 타입 → Python 타입 매핑:
        #     object {} → dict
        #     array [] → list
        #     string "" → str
        #     number   → int 또는 float
        #     true/false → True/False
        #     null     → None

    # --- 3단계: 응답 출력 ---
    print(f"  상태 코드: {res.status}")
    # HTTP 상태 코드(Status Code): 서버가 요청을 어떻게 처리했는지 알려주는 3자리 숫자.
    #   1xx: 정보 (처리 중)
    #   2xx: 성공 (200 OK, 201 Created)
    #   3xx: 리다이렉트 (301 Moved, 304 Not Modified)
    #   4xx: 클라이언트 오류 (400 Bad Request, 404 Not Found, 403 Forbidden)
    #   5xx: 서버 오류 (500 Internal Server Error, 503 Service Unavailable)

    print(f"  응답 데이터:")
    for key, value in data.items():
        print(f"    {key}: {value}")


# --- POST 요청 함수 ---

def send_post():
    """
    POST 요청으로 JSON 데이터를 서버에 보내고 응답을 출력한다.

    POST는 서버에 데이터를 "전송"하는 메서드이다.
    GET과의 핵심 차이:
      - GET: URL에만 정보 포함 (쿼리 파라미터). 길이 제한 있음(~2048자).
      - POST: 요청 본문(body)에 데이터 포함. 길이 제한 사실상 없음.
    POST는 비멱등(Non-idempotent): 같은 요청을 N번 보내면 N개의 리소스가 생길 수 있다.
    """
    print("\n" + "=" * 60)
    print("[2] POST 요청 전송")
    print("=" * 60)

    # --- 1단계: 전송할 데이터 준비 ---
    payload = {
        "student": "홍길동",
        "subject": "머신러닝(2)",
        "assignment": "과제 3 - HTTP 통신",
    }
    # payload: 네트워크 용어로 "실제 전송하려는 데이터"를 의미한다.
    #   (프로토콜 헤더 등 제어 정보를 제외한 순수 데이터 부분)
    #   지금은 Python dict이지만, 네트워크로 보내려면 바이트로 변환해야 한다.

    # --- 2단계: 직렬화 (Serialization) ---
    json_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    # 변환 과정 (Python 객체 → 네트워크 바이트):
    #
    #   dict (메모리상 객체)
    #     ↓ json.dumps()  [직렬화: 객체 → 문자열]
    #   '{"student": "홍길동", ...}'  (JSON 문자열)
    #     ↓ .encode("utf-8")  [인코딩: 문자열 → 바이트]
    #   b'{"student": "\xed\x99\x8d\xea\xb8\xb8\xeb\x8f\x99", ...}'  (바이트열)
    #
    # ensure_ascii=False: 한글을 \uXXXX로 이스케이프하지 않고 그대로 유지.
    #   True(기본값)면: "홍길동" → "\ud64d\uae38\ub3d9" (읽기 어려움)
    #   False면: "홍길동" → "홍길동" (사람이 읽을 수 있음)
    #   어느 쪽이든 서버는 정상 파싱 가능. 가독성을 위해 False 사용.

    # --- 3단계: Request 객체 생성 (POST 설정) ---
    req = urllib.request.Request(
        f"{SERVER_URL}/data",
        data=json_data,
        # data 파라미터에 바이트를 넣으면 자동으로 POST 메서드가 된다.
        # urllib의 규칙: data=None이면 GET, data가 있으면 POST.
        # 아래 method="POST"로 명시적으로도 지정하고 있다.
        headers={"Content-Type": "application/json; charset=utf-8"},
        # Content-Type 헤더: 본문의 데이터 형식을 서버에게 알려준다.
        #   이것이 없으면 서버는 본문이 JSON인지, XML인지, 폼 데이터인지 모른다.
        #   MIME 타입(Multipurpose Internet Mail Extensions)이라고도 한다.
        #     application/json — JSON 데이터
        #     text/html — HTML 문서
        #     multipart/form-data — 파일 업로드
        #   charset=utf-8: 문자 인코딩이 UTF-8임을 명시.
        method="POST",
    )

    # --- 4단계: 요청 전송 + 응답 수신 ---
    with urllib.request.urlopen(req) as res:
        # urlopen()이 하는 일 (POST 요청):
        #
        # [1] TCP 연결 수립 (3-way handshake — GET과 동일)
        #
        # [2] HTTP 요청 전송
        #     소켓에 쓰이는 실제 텍스트:
        #       POST /data HTTP/1.1\r\n
        #       Host: localhost:8080\r\n
        #       Content-Type: application/json; charset=utf-8\r\n
        #       Content-Length: 95\r\n        ← 본문 크기 (바이트 단위)
        #       \r\n                          ← 빈 줄 = 헤더 끝
        #       {"student": "홍길동", ...}    ← 본문 (POST의 핵심)
        #
        #     Content-Length가 중요한 이유:
        #       TCP는 스트림 프로토콜이다. 즉, 데이터의 "경계"가 없다.
        #       서버는 Content-Length를 보고 "본문이 여기까지"라고 판단한다.
        #       이 값이 틀리면 서버가 데이터를 잘못 읽거나 무한 대기할 수 있다.
        #
        # [3] 서버 응답 수신 + 파싱

        body = res.read().decode("utf-8")
        data = json.loads(body)
        # 역직렬화: 바이트 → 문자열 → dict (GET과 동일한 과정)

    # --- 5단계: 응답 출력 ---
    print(f"  상태 코드: {res.status}")
    print(f"  응답 데이터:")
    for key, value in data.items():
        if isinstance(value, dict):
            # 서버가 received_data를 중첩 dict로 반환하므로 한 단계 더 들어간다.
            print(f"    {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"    {key}: {value}")


# --- 메인 실행 ---

if __name__ == "__main__":
    # __name__ 가드: 이 파일이 직접 실행될 때만 아래 코드 실행.
    # import client로 불러올 때는 함수만 사용하고 자동 실행되지 않도록.
    print("서버(http://localhost:8080)에 요청을 보냅니다...\n")

    try:
        send_get()     # 1. GET 요청으로 서버 상태 확인
        send_post()    # 2. POST 요청으로 데이터 전송 + 확인
        print("\n모든 요청이 성공적으로 완료되었습니다!")

    except ConnectionRefusedError:
        # ConnectionRefusedError: TCP 연결 시도 시 서버가 응답하지 않을 때 발생.
        #   OS 수준: connect() 시스템콜이 RST(Reset) 패킷을 수신.
        #   원인: 서버가 실행 중이 아니거나, 해당 포트에서 listen하지 않음.
        #   TCP 연결의 첫 단계(SYN)에서 실패한 것이다.
        print("오류: 서버에 연결할 수 없습니다.")
        print("server.py를 먼저 실행해 주세요: python server.py")

    except Exception as e:
        # 포괄적 예외 처리: 네트워크 타임아웃, DNS 실패, HTTP 오류 등
        # 프로덕션에서는 예외 타입별로 세분화하는 것이 좋지만,
        # 학습용 코드에서는 모든 예외를 잡아서 메시지를 출력한다.
        print(f"오류 발생: {e}")

# 3단계: 실시간 양방향 통신 (WebSocket & SSE)

이 폴더에서는 파이썬의 강력한 비동기 웹 프레임워크인 **FastAPI**를 사용하여 실시간 양방향 통신인 WebSocket과 단방향 스트리밍인 SSE(Server-Sent Events)를 구현합니다.

## 🎯 학습 목표
1, 2단계에서 원시 소켓(Raw Socket)을 통해 어렵게 문자열을 파싱하고 연결을 유지했던 과정들을, 최신 프레임워크가 얼마나 쉽고 우아하게 처리(추상화)해 주는지 깨닫는 것이 목표입니다.

---

## 💻 실행 방법

### 1. 패키지 설치
이 단계부터는 외부 라이브러리가 필요합니다. 
```bash
pip install -r stage3-websocket/requirements.txt
```

### 2. 서버 실행
FastAPI 서버를 기동합니다.
```bash
cd stage3-websocket
uvicorn main:app --reload --port 8000
```

### 3. 접속 테스트
브라우저를 열고 다음 주소들에 접속하세요.

1. **WebSocket 단체 채팅방**: [http://localhost:8000/](http://localhost:8000/)
   - 브라우저 창을 2~3개 띄워놓고 한 곳에서 채팅을 치면, 모든 창에 동시에 메시지가 뿌려집니다 (브로드캐스트).
2. **SSE 실시간 시계**: [http://localhost:8000/sse](http://localhost:8000/sse)
   - 접속만 해두면 클라이언트(브라우저)가 요청하지 않아도 서버가 1초마다 지속적으로 시간을 밀어줍니다(Push).

---

### 📡 동작 흐름도 (WebSocket vs SSE)

```mermaid
sequenceDiagram
    participant Client as 웹 브라우저
    participant FastAPI as FastAPI 서버
    
    rect rgb(230, 240, 255)
    Note over Client, FastAPI: 1. WebSocket (양방향 실시간 채팅)
    Client->>FastAPI: HTTP GET (Upgrade: websocket)
    FastAPI->>Client: HTTP 101 Switching Protocols
    Client<-->>FastAPI: ws.send() & ws.receive() (자유로운 양방향 통신)
    end
    
    rect rgb(255, 240, 230)
    Note over Client, FastAPI: 2. SSE (단방향 Push 알림)
    Client->>FastAPI: HTTP GET /stream (Accept: text/event-stream)
    FastAPI->>Client: HTTP 200 OK (연결 유지)
    loop 1초마다
        FastAPI-->>Client: data: 현재 시간...\n\n (서버가 일방적으로 밀어넣음)
    end
    end
```

---

## 🔍 핵심 관전 포인트

- **프레임워크의 위력**: 2단계에서 HTTP 문자열을 파싱하기 위해 짰던 수십 줄의 코드가 `@app.get("/")` 한 줄로 끝납니다. WebSocket 핸드쉐이크(Upgrade) 역시 복잡한 규약 처리를 프레임워크가 다 해주어, 우리는 오직 "받고(receive)", "보내는(send)" 본질적인 로직에만 집중할 수 있습니다.
- **WebSocket과 SSE의 차이**:
  - **WebSocket**: `ws://` 프로토콜을 사용하며 접속이 유지되는 동안 자유롭게 데이터를 **양방향**으로 주고받습니다. (채팅, 멀티플레이어 게임 등에 적합)
  - **SSE**: 기존 `http://` 프로토콜 위에서 응답을 끊지 않고 이어가며 데이터를 **서버에서 클라이언트로 일방향**으로만 쏩니다. 미디어 타입은 `text/event-stream`을 사용합니다. (주식 호가창, 실시간 알림 등에 적합)

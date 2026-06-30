# Communication Protocols

이 프로젝트는 다양한 통신 프로토콜의 동작 원리를 학습하고, 단순한 **레이어드 아키텍처(Layered Architecture)** 기반으로 코드를 직접 구현해 보며 통신 계층의 본질을 이해하는 것을 목표로 합니다.

## 학습 커리큘럼 및 순서

학습은 저수준의 기반 통신 기술부터 고수준의 응용 계층 및 최신 트렌드 순서로 진행됩니다.

---

### 1단계: 통신의 기초와 전송 계층 (Transport Layer)
모든 고수준 프로토콜의 뼈대가 되는 계층으로, 데이터가 네트워크를 통해 어떻게 전달되는지 그 기본을 다룹니다.

* **핵심 프로토콜**: TCP, UDP
* **학습 목표**: TCP의 신뢰성 보장 메커니즘(3-Way Handshake)과 UDP의 비연결성 특징 이해

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    rect rgb(200, 220, 240)
    Note over Client, Server: TCP 3-Way Handshake (연결 지향)
    Client->>Server: SYN (연결 요청)
    Server->>Client: SYN-ACK (요청 수락 및 연결 요청)
    Client->>Server: ACK (수락 확인)
    end
    
    rect rgb(240, 220, 200)
    Note over Client, Server: UDP (비연결성)
    Client-->>Server: Datagram (핸드쉐이크 없이 데이터 즉시 전송)
    end
```

---

### 2단계: 웹 통신의 표준 (Request-Response)
현대 웹 서비스의 근간이 되는 HTTP 통신의 요청과 응답 구조를 파악합니다.

* **핵심 프로토콜**: HTTP/1.1
* **학습 목표**: 헤더(Header)와 바디(Body)의 구조, HTTP 메서드, 상태 코드, 무상태성(Stateless)의 이해

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: HTTP GET /index.html (요청)
    activate Server
    Server-->>Client: HTTP 200 OK + HTML Body (응답)
    deactivate Server
    Note over Client, Server: 기본적으로 응답 후 연결 종료 (Stateless)
```

---

### 3단계: 실시간 및 양방향 통신
HTTP의 단방향 통신 한계를 극복하고, 실시간으로 데이터를 주고받는 방법을 학습합니다.

* **핵심 프로토콜**: WebSocket, SSE (Server-Sent Events)
* **학습 목표**: HTTP를 통한 웹소켓 핸드쉐이크(Upgrade) 및 지속적인 양방향 데이터 스트림 이해

```mermaid
sequenceDiagram
    participant Client
    participant Server
    
    Note over Client, Server: 1. Handshake 단계
    Client->>Server: HTTP GET (Upgrade: websocket)
    Server->>Client: HTTP 101 Switching Protocols
    
    Note over Client, Server: 2. 양방향 통신 단계 (TCP 연결 유지)
    Client->>Server: Message Frame (Client -> Server)
    Server->>Client: Message Frame (Server -> Client)
```

---

### 4단계: 현대적인 RPC와 바이너리 통신 (Microservices)
마이크로서비스 아키텍처(MSA)에서 서비스 간 통신 효율을 극대화하기 위한 바이너리 통신 방식을 배웁니다.

* **핵심 프로토콜**: gRPC, Protocol Buffers
* **학습 목표**: JSON과 같은 텍스트 기반 직렬화와 Protobuf의 바이너리 직렬화 비교, 원격 프로시저 호출(RPC)의 개념 이해

```mermaid
flowchart LR
    Client((Client)) <--> |"바이너리 스트림 (Protobuf)<br>via HTTP/2"| Server((gRPC Server))
    
    subgraph ClientNode ["Client Node"]
    Stub[gRPC Stub]
    end
    
    subgraph ServerNode ["Server Node"]
    Service[Service Implementation]
    end
    
    Client --> Stub
    Stub -.-> Service
```

---

### 5단계: 웹의 진화와 성능 최적화 (Advanced)
웹 통신 과정에서 발생한 성능적 병목 현상을 해결하기 위한 최신 프로토콜의 발전사를 다룹니다.

* **핵심 프로토콜**: HTTP/2, HTTP/3 (QUIC)
* **학습 목표**: HTTP/2의 멀티플렉싱(Multiplexing), HTTP/3가 UDP(QUIC)를 선택한 이유 이해

```mermaid
flowchart TD
    subgraph http11 ["HTTP/1.1 (순차적 처리)"]
        direction LR
        Req1[요청 1] --> Res1[응답 1]
        Req2[요청 2] -.-> |"대기 (HOL Blocking)"| Res2[응답 2]
    end
    
    subgraph http2 ["HTTP/2 (Multiplexing)"]
        direction LR
        R1[요청 1] & R2[요청 2] & R3[요청 3] --> Stream[단일 TCP 커넥션 내 여러 스트림]
        Stream --> RS1[응답 1] & RS2[응답 2] & RS3[응답 3]
    end
```

## 아키텍처 원칙
본 프로젝트의 모든 코드는 프로토콜의 규약과 파싱 로직에 집중하기 위해, 복잡한 디자인 패턴을 배제하고 단순한 **레이어드 아키텍처(Layered Architecture)**로 구현됩니다.
- **Handler/Controller Layer**: 네트워크 소켓 통신 및 프로토콜 파싱/직렬화 담당
- **Service Layer**: 단순한 비즈니스 로직 (예: 에코, 메시지 브로드캐스팅 등) 처리
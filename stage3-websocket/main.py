from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from managers.connection_manager import manager
from managers.sse_manager import event_generator

app = FastAPI()

# ==========================================
# 1. HTML View (테스트 클라이언트 화면)
# ==========================================
html_chat = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Chat</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #f9f9f9; }
            .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            ul { list-style-type: none; padding: 0; }
            li { background: #e3f2fd; margin: 5px 0; padding: 10px; border-radius: 5px; }
            input { padding: 10px; width: 300px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>WebSocket 단체 채팅방 💬</h1>
            <p>이 창을 여러 개 띄워놓고 채팅을 쳐보세요!</p>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off" placeholder="메시지 입력..."/>
                <button>Send</button>
            </form>
            <ul id='messages'></ul>
            <br>
            <a href="/sse">SSE 실시간 시계 보러가기</a>
        </div>
        <script>
            // 브라우저 내장 WebSocket API 사용 (HTTP -> WS 업그레이드 요청)
            var client_id = Date.now();
            var ws = new WebSocket("ws://localhost:8000/ws/" + client_id);
            
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value); // 서버로 메시지 전송
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

html_sse = """
<!DOCTYPE html>
<html>
    <head>
        <title>SSE Time Ticker</title>
        <style>
            body { font-family: sans-serif; padding: 20px; background: #f9f9f9; }
            .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
            #result { padding: 20px; background: #333; color: #0f0; font-size: 24px; font-family: monospace; border-radius: 8px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>SSE (Server-Sent Events) 실시간 시계 ⏱️</h1>
            <p>클라이언트(브라우저)가 요청하지 않아도 서버가 일방적으로 데이터를 계속 밀어줍니다.</p>
            <div id="result">Waiting for server...</div>
            <br>
            <a href="/">WebSocket 채팅방 보러가기</a>
        </div>
        <script>
            // 브라우저 내장 EventSource API 사용
            var source = new EventSource("/stream");
            source.onmessage = function(event) {
                document.getElementById("result").innerHTML = event.data;
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get_chat():
    return HTMLResponse(html_chat)

@app.get("/sse")
async def get_sse():
    return HTMLResponse(html_sse)


# ==========================================
# 2. WebSocket 엔드포인트 (양방향)
# ==========================================
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    # 연결 수락 및 매니저 등록
    await manager.connect(websocket)
    await manager.broadcast(f"🎉 Client #{client_id} 님이 입장하셨습니다.")
    try:
        # 1, 2단계의 거친 raw 소켓 루프 대신 우아한 비동기 웹소켓 처리
        while True:
            data = await websocket.receive_text()
            # 누군가 메시지를 보내면 접속한 모두에게 브로드캐스트
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        # 클라이언트 연결이 끊어지면 매니저에서 제거
        manager.disconnect(websocket)
        await manager.broadcast(f"👋 Client #{client_id} 님이 퇴장하셨습니다.")


# ==========================================
# 3. SSE 엔드포인트 (단방향)
# ==========================================
@app.get("/stream")
async def message_stream():
    # 미디어 타입을 text/event-stream 으로 설정하여 응답
    # event_generator()는 비동기적으로 1초마다 텍스트를 yield 합니다.
    return StreamingResponse(event_generator(), media_type="text/event-stream")

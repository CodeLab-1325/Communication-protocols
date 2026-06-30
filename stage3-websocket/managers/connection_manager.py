from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # 현재 연결된 활성 웹소켓 클라이언트들을 저장하는 리스트
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # HTTP를 웹소켓으로 업그레이드(Handshake) 승인
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # 연결 해제 시 리스트에서 제거
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # 접속한 모든 클라이언트에게 비동기로 메시지 전송
        for connection in self.active_connections:
            await connection.send_text(message)

# 싱글톤 인스턴스로 사용
manager = ConnectionManager()

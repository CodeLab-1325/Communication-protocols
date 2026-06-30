import socket

def run_server(host='127.0.0.1', port=3000):
    # 1. 소켓 생성 (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # 포트 재사용 옵션 (서버 재시작 시 Address already in use 에러 방지)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 2. 호스트와 포트 바인딩
        server_socket.bind((host, port))
        
        # 3. 연결 대기 (Listening)
        server_socket.listen()
        print(f"[TCP Server] Listening on {host}:{port}...")
        
        while True:
            # 4. 클라이언트 연결 수락 (블로킹됨)
            conn, addr = server_socket.accept()
            with conn:
                print(f"[TCP Server] Connected by {addr}")
                while True:
                    # 5. 데이터 수신
                    data = conn.recv(1024)
                    if not data:
                        # 클라이언트가 연결을 끊으면 루프 탈출
                        break
                    
                    print(f"[TCP Server] Received: {data.decode('utf-8')}")
                    
                    # 6. 데이터 송신 (Echo)
                    conn.sendall(data)
                print(f"[TCP Server] Connection closed by {addr}")

if __name__ == '__main__':
    run_server()

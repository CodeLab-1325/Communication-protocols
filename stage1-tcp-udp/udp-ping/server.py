import socket

def run_server(host='127.0.0.1', port=4000):
    # 1. 소켓 생성 (IPv4, UDP)
    # SOCK_DGRAM은 데이터그램(UDP)을 의미합니다.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # 2. 호스트와 포트 바인딩
        # UDP는 연결(listen/accept) 과정 없이 바인딩만으로 준비가 끝납니다.
        server_socket.bind((host, port))
        print(f"[UDP Server] Ready and receiving on {host}:{port}...")
        
        while True:
            # 3. 데이터 수신 (블로킹됨)
            # 데이터를 보낸 클라이언트의 주소(addr)도 함께 받습니다.
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"[UDP Server] Received '{message}' from {addr}")
            
            # 4. 응답 전송 (Pong)
            if message.strip().upper() == "PING":
                reply = "PONG"
            else:
                reply = f"ECHO: {message}"
                
            # TCP처럼 연결된 커넥션 객체가 없으므로, 매번 목적지 주소를 명시해야 합니다.
            server_socket.sendto(reply.encode('utf-8'), addr)

if __name__ == '__main__':
    run_server()

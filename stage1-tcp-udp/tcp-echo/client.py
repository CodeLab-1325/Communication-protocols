import socket
import time

def run_client(host='127.0.0.1', port=3000):
    # 1. 소켓 생성 (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        print(f"[TCP Client] Connecting to {host}:{port}...")
        # 2. 서버에 연결 요청 (SYN - SYN/ACK - ACK)
        client_socket.connect((host, port))
        print("[TCP Client] Connected!")
        
        messages = ["Hello, Server!", "This is a TCP test.", "Goodbye!"]
        
        for msg in messages:
            print(f"[TCP Client] Sending: {msg}")
            # 3. 데이터 송신
            client_socket.sendall(msg.encode('utf-8'))
            
            # 4. 데이터 수신
            data = client_socket.recv(1024)
            print(f"[TCP Client] Received: {data.decode('utf-8')}")
            
            time.sleep(1)

if __name__ == '__main__':
    run_client()

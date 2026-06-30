import socket
import time

def run_client(host='127.0.0.1', port=4000):
    # 1. 소켓 생성 (IPv4, UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        
        # 타임아웃 설정 (UDP는 응답이 안 올 수도 있으므로 무한 대기 방지)
        client_socket.settimeout(2.0)
        
        messages = ["PING", "Hello UDP", "PING"]
        
        for msg in messages:
            print(f"\n[UDP Client] Sending: {msg}")
            
            # 2. 데이터 송신
            # UDP는 connect() 과정 없이 곧바로 목적지 주소를 적어서 던집니다.
            client_socket.sendto(msg.encode('utf-8'), (host, port))
            
            try:
                # 3. 응답 대기
                data, server_addr = client_socket.recvfrom(1024)
                print(f"[UDP Client] Received '{data.decode('utf-8')}' from {server_addr}")
            except socket.timeout:
                print("[UDP Client] Request timed out (No response)")
                
            time.sleep(1)

if __name__ == '__main__':
    run_client()

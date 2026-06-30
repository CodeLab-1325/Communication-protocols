import socket
from http_parser import parse_request
from router import route
from http_response import serialize_response

def run_server(host='0.0.0.0', port=8080):
    # 1. 1단계와 동일하게 TCP 소켓을 생성하고 대기합니다.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        
        print(f"🚀 [Raw HTTP Server] Started!")
        print(f"👉 브라우저를 열고 http://localhost:{port}/ 에 접속해 보세요.\n")
        
        while True:
            conn, addr = server_socket.accept()
            with conn:
                # [A] 브라우저(클라이언트)가 보낸 Raw 데이터 수신
                # 브라우저는 접속하자마자 HTTP 규약에 맞춘 텍스트 데이터를 쏟아냅니다.
                raw_data = conn.recv(4096)
                if not raw_data:
                    continue
                    
                # [B] 파싱 계층 (Parser Layer)
                # 복잡한 문자열 텍스트를 파이썬 객체(HttpRequest)로 예쁘게 파싱합니다.
                req = parse_request(raw_data)
                
                # 콘솔에 브라우저가 보낸 정보 출력 (확인용)
                print(f"[{addr[0]}] 요청됨: {req.method} {req.path}")
                print(f" - 사용 브라우저(User-Agent): {req.headers.get('User-Agent', 'Unknown')}")
                
                # [C] 라우팅 및 비즈니스 로직 계층 (Controller/Handler Layer)
                # 요청 경로에 맞는 함수를 실행하고 결과 객체(HttpResponse)를 돌려받습니다.
                res = route(req)
                
                # [D] 직렬화 계층 (Serializer Layer)
                # 파이썬 객체로 만들어진 결과를 다시 브라우저가 이해할 수 있는 날것의 HTTP 텍스트로 변환합니다.
                raw_response = serialize_response(res)
                
                # [E] 브라우저로 최종 전송
                conn.sendall(raw_response)
                
                # 전송이 끝나면 'with conn:' 블록이 끝나면서 자동으로 소켓(conn)이 닫힙니다.
                # HTTP/1.1의 기본은 연결을 닫지 않고 유지(Keep-Alive)하는 것이지만,
                # 본 예제에서는 구현을 단순화하기 위해 매번 닫도록(Connection: close) 설정했습니다.

if __name__ == '__main__':
    run_server()

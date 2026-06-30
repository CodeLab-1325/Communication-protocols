class HttpResponse:
    def __init__(self, status_code: int = 200, status_text: str = "OK", content_type: str = "text/plain", body: str = ""):
        self.status_code = status_code
        self.status_text = status_text
        self.content_type = content_type
        self.body = body
        # HTTP 필수 헤더 설정
        self.headers = {
            "Content-Type": f"{self.content_type}; charset=utf-8",
            "Content-Length": str(len(self.body.encode('utf-8'))),
            "Connection": "close"  # 응답 후 소켓 연결 종료 지시
        }

def serialize_response(res: HttpResponse) -> bytes:
    """
    파이썬 객체로 만들어진 응답 정보를
    실제 네트워크(TCP 소켓)로 전송할 수 있는 HTTP 규약 문자열(Bytes)로 변환합니다.
    """
    # 1. Response Line 생성 (예: HTTP/1.1 200 OK)
    response_line = f"HTTP/1.1 {res.status_code} {res.status_text}\r\n"
    
    # 2. Headers 생성 (예: Content-Type: text/html\r\n)
    headers_str = ""
    for key, value in res.headers.items():
        headers_str += f"{key}: {value}\r\n"
        
    # 3. 헤더의 끝을 알리는 빈 줄(\r\n) 추가 후 Body 결합
    full_response = response_line + headers_str + "\r\n" + res.body
    
    # 4. 문자열을 바이트로 인코딩하여 반환
    return full_response.encode('utf-8')

class HttpRequest:
    def __init__(self, method: str, path: str, version: str, headers: dict, body: str):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body

def parse_request(raw_data: bytes) -> HttpRequest:
    """
    네트워크(TCP 소켓)를 통해 들어온 날것의 바이트(Bytes) 데이터를
    우리가 다루기 쉬운 파이썬 객체로 파싱합니다.
    """
    # 1. 바이트 데이터를 문자열로 디코딩
    try:
        text_data = raw_data.decode('utf-8')
    except UnicodeDecodeError:
        text_data = ""
        
    # 2. HTTP 규약상 헤더와 바디는 빈 줄(\r\n\r\n)로 구분됩니다.
    parts = text_data.split('\r\n\r\n', 1)
    header_part = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    
    # 3. 헤더 부분을 한 줄씩(\r\n) 분리
    lines = header_part.split('\r\n')
    if not lines or not lines[0]:
        return HttpRequest("", "", "", {}, "")
        
    # 4. 첫 번째 줄은 Request Line (예: GET / HTTP/1.1)
    request_line = lines[0].split(' ')
    method = request_line[0] if len(request_line) > 0 else ""
    path = request_line[1] if len(request_line) > 1 else ""
    version = request_line[2] if len(request_line) > 2 else ""
    
    # 5. 두 번째 줄부터는 Headers
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
            
    return HttpRequest(method, path, version, headers, body)

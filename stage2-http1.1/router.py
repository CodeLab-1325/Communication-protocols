from handlers import home_handler, api_handler, not_found_handler
from http_parser import HttpRequest
from http_response import HttpResponse

def route(req: HttpRequest) -> HttpResponse:
    """
    클라이언트가 요청한 URL(path)과 HTTP 메서드에 따라
    어떤 비즈니스 로직(Handler)을 실행할지 결정(Routing)합니다.
    """
    if req.method == "GET" and req.path == "/":
        return home_handler(req)
        
    elif req.method == "GET" and req.path == "/api/data":
        return api_handler(req)
        
    else:
        # 매칭되는 경로가 없으면 404 Not Found 처리
        return not_found_handler(req)

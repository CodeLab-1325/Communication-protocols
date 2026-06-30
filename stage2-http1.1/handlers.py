from http_response import HttpResponse

def home_handler(req) -> HttpResponse:
    html = """
    <html>
        <head>
            <title>Raw HTTP Server</title>
            <style>
                body { font-family: sans-serif; padding: 40px; background-color: #f4f4f9; }
                .box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="box">
                <h1>Hello, HTTP Protocol! 🚀</h1>
                <p>이 웹페이지는 Django나 FastAPI 같은 <strong>웹 프레임워크를 전혀 사용하지 않고</strong>, 오직 Raw Socket만을 통해 HTTP 규약을 직접 조립해서 브라우저로 렌더링된 화면입니다.</p>
                <p>터미널을 확인해보시면 브라우저가 몰래 보낸 복잡한 HTTP 요청 헤더들을 보실 수 있습니다!</p>
                <a href="/api/data">JSON API 테스트 해보기</a>
            </div>
        </body>
    </html>
    """
    return HttpResponse(status_code=200, status_text="OK", content_type="text/html", body=html)

def api_handler(req) -> HttpResponse:
    json_data = '{"message": "Welcome to Raw HTTP API", "status": "success", "framework": "none"}'
    return HttpResponse(status_code=200, status_text="OK", content_type="application/json", body=json_data)

def not_found_handler(req) -> HttpResponse:
    return HttpResponse(status_code=404, status_text="Not Found", content_type="text/plain", body="404 Page Not Found: 잘못된 경로입니다.")

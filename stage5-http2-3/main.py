from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
import asyncio

app = FastAPI()

@app.get("/")
async def index():
    # 수십 개의 리소스 요청을 발생시키는 HTML을 반환합니다.
    # HTTP/1.1 에서는 커넥션(일반적으로 6개) 제한으로 인해 Waterfall 차트가 계단식(HOL Blocking)으로 나타나지만,
    # HTTP/2 에서는 1개의 커넥션으로 수십 개의 요청이 동시에(Multiplexing) 처리되는 것을 볼 수 있습니다.
    
    images_html = ""
    # 30개의 더미 리소스를 요청하도록 img 태그 생성
    for i in range(1, 31):
        images_html += f'<div class="box"><img src="/api/resource/{i}" width="100" height="100" alt="Res {i}"></div>\n'

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTTP/2 Multiplexing Test</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; }}
            .container {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }}
            .box {{ background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .instruction {{ background: #fff3cd; padding: 15px; border-left: 5px solid #ffc107; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <h1>HTTP/2 멀티플렉싱(Multiplexing) 테스트 🚀</h1>
        
        <div class="instruction">
            <h3>👀 이렇게 확인해 보세요!</h3>
            <ol>
                <li>브라우저의 <strong>개발자 도구(F12)</strong>를 엽니다.</li>
                <li><strong>Network(네트워크) 탭</strong>으로 이동합니다.</li>
                <li>컬럼 이름(Name, Status 등)을 우클릭하여 <strong>Protocol</strong> 항목이 보이도록 체크합니다.</li>
                <li>F5를 눌러 새로고침합니다.</li>
                <li><strong>Protocol이 <code>h2</code></strong>로 찍히며, 30개의 이미지가 폭포수(Waterfall) 탭에서 <strong>가로로 똑같이 줄을 서서 동시에(병렬로)</strong> 로딩되는 장관을 확인하세요!</li>
            </ol>
        </div>
        
        <div class="container">
            {images_html}
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_content)


@app.get("/api/resource/{resource_id}")
async def get_resource(resource_id: int):
    # 인위적인 네트워크 지연(Delay) 추가
    # HTTP/1.1이라면 앞선 리소스 요청이 지연되는 동안 뒤의 리소스 요청들은 서버로 출발조차 못하고 대기합니다.
    await asyncio.sleep(0.2)
    
    # SVG 이미지 문자열을 즉석에서 생성하여 반환 (네트워크 트래픽 유발용)
    svg_content = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
        <rect width="100" height="100" fill="#4caf50" rx="10"/>
        <text x="50" y="50" font-size="20" text-anchor="middle" alignment-baseline="middle" fill="white">Image {resource_id}</text>
    </svg>
    """
    return Response(content=svg_content, media_type="image/svg+xml")

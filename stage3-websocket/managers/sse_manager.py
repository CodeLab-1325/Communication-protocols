import asyncio
from datetime import datetime

async def event_generator():
    """
    1초마다 현재 시간을 생성하여(yield) 클라이언트로 계속 밀어넣는(Push) 비동기 제너레이터입니다.
    """
    while True:
        # SSE 데이터는 반드시 "data: {메시지}\n\n" 형식을 맞춰야 브라우저가 인식합니다.
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield f"data: 현재 서버 시간은 {now} 입니다.\n\n"
        
        # 1초 대기 (비동기 블로킹 없이)
        await asyncio.sleep(1)

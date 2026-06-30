import grpc
from concurrent import futures
import sys
import os

# 현재 디렉토리와 protos 디렉토리를 path에 추가하여 자동 생성된 모듈을 찾을 수 있게 함
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'protos')))

# 주의: 이 파일들은 아래 명령어로 미리 컴파일(생성)되어 있어야 합니다!
# python -m grpc_tools.protoc -I. --python_out=./protos --grpc_python_out=./protos protos/user.proto
try:
    import user_pb2
    import user_pb2_grpc
except ImportError:
    print("❌ 에러: user_pb2 모듈을 찾을 수 없습니다. README.md를 읽고 .proto 파일을 먼저 컴파일해주세요!")
    sys.exit(1)

# 1. 가짜 데이터베이스 (실제 환경에서는 DB에서 조회)
MOCK_DB = {
    1: {"name": "Alice", "email": "alice@example.com", "is_active": True},
    2: {"name": "Bob", "email": "bob@example.com", "is_active": False},
}

# 2. 비즈니스 로직 계층 (자동 생성된 Servicer 스켈레톤 클래스를 상속)
class UserService(user_pb2_grpc.UserServiceServicer):
    
    # proto 파일에 정의했던 GetUser 함수를 실제로 구현
    def GetUser(self, request, context):
        print(f"[Server] Received request for User ID: {request.user_id}")
        
        user_data = MOCK_DB.get(request.user_id)
        
        if user_data:
            # 성공 시 UserResponse 객체 반환
            return user_pb2.UserResponse(
                user_id=request.user_id,
                name=user_data["name"],
                email=user_data["email"],
                is_active=user_data["is_active"]
            )
        else:
            # 실패 시 gRPC 상태 코드와 에러 메시지 반환 (HTTP의 404와 유사)
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found in MOCK_DB")

def serve():
    # 3. gRPC 서버 생성 (동시 처리를 위한 스레드 풀 할당)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # 4. 우리가 만든 비즈니스 로직(UserService)을 서버 라우터에 등록
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    
    # 5. 50051 포트 개방 및 서버 기동
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 [gRPC Server] Started on port 50051...")
    
    # 서버가 바로 종료되지 않도록 대기
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

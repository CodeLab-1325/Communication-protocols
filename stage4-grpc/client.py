import grpc
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'protos')))

try:
    import user_pb2
    import user_pb2_grpc
except ImportError:
    print("❌ 에러: user_pb2 모듈을 찾을 수 없습니다. README.md를 읽고 .proto 파일을 먼저 컴파일해주세요!")
    sys.exit(1)

def run_client():
    print("🔌 [gRPC Client] Connecting to server...")
    
    # 1. 50051 포트로 gRPC 통신 채널 생성 (HTTP/2 기반)
    with grpc.insecure_channel('localhost:50051') as channel:
        
        # 2. Stub(분신) 생성: 이 Stub을 통해 원격 서버 함수를 로컬 함수처럼 호출 가능
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # 3. 통신 테스트 1: 존재하는 유저 조회
        print("\n--- Test 1: Fetching User 1 ---")
        request = user_pb2.UserRequest(user_id=1)
        try:
            # 로컬 함수처럼 stub.GetUser() 호출!
            # (내부적으로 파라미터를 바이너리로 직렬화하여 네트워크로 보내고, 결과를 역직렬화해서 가져옴)
            response = stub.GetUser(request)
            print("✅ Success! Received Data:")
            print(f" - ID: {response.user_id}")
            print(f" - Name: {response.name}")
            print(f" - Email: {response.email}")
            print(f" - Active: {response.is_active}")
        except grpc.RpcError as e:
            print(f"❌ Failed: {e.details()} (Code: {e.code()})")
            
        # 4. 통신 테스트 2: 존재하지 않는 유저 조회
        print("\n--- Test 2: Fetching User 99 (Not Exists) ---")
        request = user_pb2.UserRequest(user_id=99)
        try:
            response = stub.GetUser(request)
            print(f"✅ Success! Received: {response.name}")
        except grpc.RpcError as e:
            # 서버가 abort로 보낸 NOT_FOUND 에러를 잡아서 처리합니다.
            print(f"❌ Failed (As expected): {e.details()} (Code: {e.code()})")

if __name__ == '__main__':
    run_client()

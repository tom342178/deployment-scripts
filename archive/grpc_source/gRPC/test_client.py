

import grpc
import test_pb2
import test_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = test_pb2_grpc.MyServiceStub(channel)

    request = test_pb2.MyRequest()
    request.message_content = "Hello, Server!"

    # Set request fields

    response = stub.MyMethod(request)
    # Process the response

    pass

if __name__ == '__main__':
    run()



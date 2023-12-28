

from concurrent import futures
import grpc
import test_pb2
import test_pb2_grpc
from grpc_reflection.v1alpha import reflection


class MyServiceServicer(test_pb2_grpc.MyServiceServicer):
    def MyMethod(self, request, context):
        # Implement your service logic here
        request_data = request.message_content
        response = test_pb2.MyResponse()
        response.serialized_data.extend(["test_val_1", "test_val_2", "test_val_3"])

        # Set response fields
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)

    # Add reflection service to the server
    SERVICE_NAMES = (
        test_pb2.DESCRIPTOR.services_by_name['MyService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


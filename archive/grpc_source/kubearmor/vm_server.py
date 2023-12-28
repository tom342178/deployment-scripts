import grpc
import concurrent.futures
import vm_pb2
import vm_pb2_grpc
from grpc_reflection.v1alpha import reflection


class CliHandlerServicer(vm_pb2_grpc.HandleCliServicer):
    def HandleCliRequest(self, request, context):
        # Implement your gRPC method logic here
        response = vm_pb2.ResponseStatus()
        response.ScriptData = f"Received request for KVM: {request.KvmName}"
        response.StatusMsg = "Success"
        response.Status = 200
        return response

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    vm_pb2_grpc.add_HandleCliServicer_to_server(CliHandlerServicer(), server)

    # Add reflection service to the server
    SERVICE_NAMES = (
        vm_pb2.DESCRIPTOR.services_by_name['HandleCli'].full_name, reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)


    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

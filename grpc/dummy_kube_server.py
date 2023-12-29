import argparse
import grpc
import datetime
import time
import random
import kubearmor.kubearmor_pb2 as kubearmor_pb2
import kubearmor.kubearmor_pb2_grpc as kubearmor_pb2_grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection


# Implement the LogService
class LogService(kubearmor_pb2_grpc.LogServiceServicer):
    def HealthCheck(self, request, context):
        # Implement your logic here
        value_received = request.nonce

        reply_obj = kubearmor_pb2.ReplyMessage(Retval=value_received)

        return reply_obj

    def WatchMessages(self, request, context):
        # Implement your logic here
        yield kubearmor_pb2.Message()

    def WatchAlerts(self, request, context):
        # Implement your logic here
        yield kubearmor_pb2.Alert()

    def WatchLogs(self, request, context):
        # Implement your logic here
        # yield kubearmor_pb2.Log()

        request_data = request.Filter

        response = kubearmor_pb2.Log()

        # response.Labels = "Labels Data"
        # response.ProcessName = "Process Test"

        #response.serialized_data.extend(["test_val_1", "test_val_2", "test_val_3"])

        # Set response fields
        for _ in range (1):
            timestamp_int = time.time()
            timestamp = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y-%m-%d %H:%M:%s.%f')
            timestamp_int = int(timestamp_int)

            if request.Filter in ["alert", "log", "all"]:
                response.Timestamp = timestamp_int  # 1
                response.UpdatedTime = timestamp  # 2

                response.ClusterName = random.choice(["default", "kubearmor"])  # 3
                response.HostName = "minikube"  # 4

                response.NamespaceName = random.choice(["default", "kubearmor"])  # 5
                # response.Owner = "map[Name:nginx Namespace:default Ref:Deployment]" # 24
                response.PodName = "nginx-7854ff8877-k4tsj"  # 6
                response.Labels = "app=nginx"  # 23

                response.ContainerID = "cf3e3217059a56e21ca4cf676572ffb0aac66f0182fa107d239ce4636e53c396"  # 7
                response.ContainerName = "nginx"  # 8
                response.ContainerImage = "nginx:latest@sha256:2bdc49f2f8ae8d8dc50ed00f2ee56d00385c6f8bc8a8b320d0a294d9e3b49026"  # 19

                response.ParentProcessName = "/usr/bin/bash"  # 20
                response.ProcessName = "/usr/bin/apt-get"  # 21

                response.HostPPID = random.randrange(4000, 5000)  # 22
                response.HostPID = random.randrange(4000, 5000)  # 9
                response.PPID = random.randrange(4000, 5000)  # 10
                response.PID = random.randrange(4000, 5000)  # 11
                response.UID = random.randrange(0, 6)  # 12

                response.Type = "MatchedPolicy"  # 13
                response.Source = "/usr/bin/bash"  # 14
                response.Operation = "Process"  # 15
                response.Resource = f"/usr/bin/apt-get -y {random.choice(["curl", "update", "upgrade", "wget"])}"  # 16
                response.Data = "syscall=SYS_EXECVE"  # 17

            response.Result = random.choice(["Passed", "Failed"])  # 18

            if request.Filter in ["alert", "all"]:
                response.PolicyName = "block-pkg-mgmt-tools-exec"  # 13
                response.Severity = random.randrange(0, 4)  # 14
                response.Action = "Audit (Block)"  # 22
                response.Enforcer = "eBPF Monitor"  # 28

            yield response
            time.sleep(0.5)

# Implement the PushLogService
class PushLogService(kubearmor_pb2_grpc.PushLogServiceServicer):
    def HealthCheck(self, request, context):
        # Implement your logic here
        return kubearmor_pb2.ReplyMessage(Retval=0)

    def PushMessages(self, request_iterator, context):
        for message in request_iterator:
            # Implement your logic here
            yield kubearmor_pb2.ReplyMessage(Retval=0)

    def PushAlerts(self, request_iterator, context):
        for alert in request_iterator:
            # Implement your logic here
            yield kubearmor_pb2.ReplyMessage(Retval=0)

    def PushLogs(self, request_iterator, context):
        for log in request_iterator:
            # Implement your logic here
            yield kubearmor_pb2.ReplyMessage(Retval=0)

def server():
    """
    Dummy server to work against kubearmor.proto for testing.
    :args:
        --port      Port for dummy server (default: 50051)
    """
    parse = argparse.ArgumentParser()
    parse.add_argument('--port', type=int, default=50051, help="Port for dummy server")
    args = parse.parse_args()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kubearmor_pb2_grpc.add_LogServiceServicer_to_server(LogService(), server)
    kubearmor_pb2_grpc.add_PushLogServiceServicer_to_server(PushLogService(), server)

    # Add reflection service to the server
    SERVICE_NAMES = (
        kubearmor_pb2.DESCRIPTOR.services_by_name['LogService'].full_name, reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()

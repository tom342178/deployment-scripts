import argparse
import grpc
from concurrent import futures
import dummy_pb2
import dummy_pb2_grpc
import json
import random
import time

SAMPLE_DATA = [
    "hello world",
    10,
    35.65,
    True,
    [1,2,3.4],
    {"Timestamp":1702313177,"UpdatedTime":"2023-12-11T16:46:17.846500Z","ClusterName":"default","HostName":"aks-agentpool-84859103-vmss000000","NamespaceName":"calico-system","Owner":{"Ref":"DaemonSet","Name":"calico-node","Namespace":"calico-system"},"PodName":"calico-node-xbx6f","Labels":"app.kubernetes.io/name=calico-node,k8s-app=calico-node","ContainerID":"071cbc16ada66cc52c6b4904bbc3c76e1b557e71e744e229bcae3e27e8912ce4","ContainerName":"calico-node","ContainerImage":"mcr.microsoft.com/oss/calico/node:v3.24.6sha256:3560b5bfbdb6a0e4eb4625bf2548ba3160a13cb63136697250860fccf2a23640","HostPPID":5323,"HostPID":5330,"PPID":54,"PID":61,"UID":0,"Type":"ContainerLog","Operation":"Network","Resource":"remoteip=127.0.0.1 port=9099 protocol=TCP","Data":"kprobe=tcp_accept domain=AF_INET","Result":"Passed"},
    {"ClusterName":"default","HostName":"aks-bahnodepool-23812902-vmss000001","PPID":0,"UID":0},
    {"kvlistValue": { "values": [
        {"key": "HostPID", "value": {"doubleValue": 261}},
        {"key": "PPID", "value": {"doubleValue": 1}},
        {"key": "Operation", "value": {"stringValue": "File"}},
        {"key": "Resource", "value": {"stringValue": "/var/log/journal/b09389c7d40f420982b5facb1f6e1686"}},
        {"key": "Data", "value": {"stringValue": "syscall=SYS_OPENAT fd=-100 flags=O_RDONLY|O_NONBLOCK|O_DIRECTORY|O_CLOEXEC"}},
        {"key": "Result", "value": {"stringValue": "Passed"}},
        {"key": "UpdatedTime", "value": {"stringValue": "2023-03-27T11:10:26.485913Z"}},
        {"key": "HostName", "value": {"stringValue": "babe-chinwendum"}},
        {"key": "PID", "value": {"doubleValue": 261}},
        {"key": "Type", "value": {"stringValue": "HostLog"}},
        {"key": "Source", "value": {"stringValue": "/usr/lib/systemd/systemd-journald"}}
    ]}}
]


def create_server():
    """
    Create a gRPC server with a thread pool.
    """
    try:
        return grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    except Exception as error:
        print(f"Failed to start server (Error: {error})")
        exit(1)


class SerializeService(dummy_pb2_grpc.SerializeServiceServicer):
    # send one once and done
    # def GetSampleData(self, request, context):
    #     # Serialize Python dictionaries to strings
    #     serialized_data_list = [json.dumps(data) for data in SAMPLE_DATA]
    #
    #     # Return the serialized data in the response
    #     return dummy_pb2.SampleDataResponse(serialized_data=serialized_data_list)

    def GetSampleData(self, request, context):
        # Serialize Python dictionaries to strings
        serialized_data_list = [json.dumps(data) for data in SAMPLE_DATA]

        row = random.choice(serialized_data_list)
        # Return the serialized data in the response
        response = dummy_pb2.SampleDataResponse(serialized_data=[row])

        time.sleep(random.choice(range(10, 31)))
        return response


def run_server(port: int):
    # Create a gRPC server
    server = create_server()

    # Add the SerializeService implementation to the server
    dummy_pb2_grpc.add_SerializeServiceServicer_to_server(SerializeService(), server)

    # Set up an insecure port for the server to listen on
    server.add_insecure_port(f'[::]:{port}')

    # Start the server
    server.start()
    print(f"Server started. Listening on port {port}...")

    # try:
    server.wait_for_termination()
    # except KeyboardInterrupt:
    #     server.stop()


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--port', type=int, default=50051)
    args = parse.parse_args()

    run_server(port=args.port)


if __name__ == '__main__':
    main()

import argparse
import grpc
#import dummy_pb2
#import dummy_pb2_grpc
import vm_pb2
import vm_pb2_grpc
import json
import time
import threading
from kubernetes_api import KubernetesInfo
from port_forwarding import PortForwardingService


def create_channel(conn:str, credentials:dict=None):
    """
    Create a gRPC channel against another machine.
    """
    channel = None
    if credentials is not None:
        try:
            channel = grpc.secure_channel(target=conn, credentials=credentials)
        except Exception as error:
            print(f"Failed to create a secure channel against {conn} (Error: {error})")
            exit(1)
    else:
        try:
            channel = grpc.insecure_channel(target=conn)
        except Exception as error:
            print(f"Failed to create an insecure channel against {conn} (Error: {error})")
            exit(1)
    if channel is None:
        print(f"Failed to create a channel connection against {conn}")
        exit(1)

    return channel


def __close_channel(channel):
    try:
        channel.close()
    except Exception as error:
        print(f"Failed to close channel (Error: {error})")


def set_stub(channel):
    """
    Create a service connection.
    """
    try:
        return vm_pb2_grpc.HandleCliStub(channel)
    except Exception as error:
        print(f"Failed to create a stub against the channel (Error: {error})")
        exit(1)


def execute_service(stub):
    """
    Execute the service.
    """
    deserialized_data_list = []
    try:
        response = stub.HandleCliRequest(vm_pb2.ResponseStatus())
    except Exception as error:
        print(f"Failed to execute the service (Error: {error})")
    else:
        try:
            serialized_data_list = response.serialized_data
        except Exception as error:
            print(f"Failed to get serialized data (Error: {error})")
        else:
            deserialized_data_list = [json.loads(data) for data in serialized_data_list]

    return deserialized_data_list


def main():
    k8s_port = 32767
    match_labels = {"kubearmor-app": "kubearmor-relay"}
    target_service = "kubearmor-relay"

    k8sInfo = KubernetesInfo(match_labels=match_labels, target_service=target_service)
    k8sInfo.create_client()
    pod_name, namespace = k8sInfo.get_pod_name()
    forwarding_port = k8sInfo.get_local_port()
    # Create a channel to connect to the server
    channel = create_channel(conn=f"localhost:{k8s_port}")

    # Associate the stub with the server and allow the client to make RPC calls
    stub = set_stub(channel=channel)

    port_forwarding_service = PortForwardingService(local_port=forwarding_port, remote_host='localhost', remote_port=k8s_port)

    port_forwarding_thread = threading.Thread(target=port_forwarding_service.start_port_forwarding)
    port_forwarding_thread.start()


    while True:
        # Execute the service
        deserialized_data = execute_service(stub=stub)
        print(deserialized_data)
        time.sleep(10)



if __name__ == '__main__':
    main()

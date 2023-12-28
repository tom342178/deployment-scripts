import os
import random
import socket
import subprocess
import threading

from kubernetes import client, config
from kubernetes.client import ApiException, rest
# from kubernetes.client.rest import rest

class PortForwardingService:
    def __init__(self, local_port, remote_host, remote_port):
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port

    def start_port_forwarding(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.local_port))
        server.listen(5)

        print(f"[*] Listening on 0.0.0.0:{self.local_port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            client_handler = threading.Thread(
                target=self.__handle_client,
                args=(client_socket,)
            )
            client_handler.start()

    def __handle_client(self, client_socket):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((self.remote_host, self.remote_port))

        while True:
            # Receive data from the client
            client_data = client_socket.recv(4096)
            if not client_data:
                break

            # Forward the data to the remote server
            remote_socket.sendall(client_data)

            # Receive the response from the remote server
            remote_data = remote_socket.recv(4096)
            if not remote_data:
                break

            # Forward the response to the client
            client_socket.sendall(remote_data)

        client_socket.close()
        remote_socket.close()


# def main():
#     """
#     k8s_port:int - Port used by kubernetes
#     forwarding_port:int - Port forwarded to
#     """
#     conn = create_k8s_client()
#     k8s_port = 32767
#     match_labels = {"kubearmor-app": "kubearmor-relay"}
#     target_service = "kubearmor-relay"
#
#     k8sInfo = KubernetesInfo(match_labels=match_labels, target_service=target_service)
#     k8sInfo.create_client()
#     pod_name, namespace = k8sInfo.get_pod_name()
#     forwarding_port = k8sInfo.get_local_port()
#
#     start_port_forwarding(local_port=forwarding_port, remote_host='localhost', remote_port=k8s_port)
#
# if __name__ == '__main__':
#     main()



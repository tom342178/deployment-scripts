import os
import random
import socket
import subprocess
import threading

from kubernetes import client, config
from kubernetes.client import ApiException, rest
# from kubernetes.client.rest import rest


class KubernetesInfo:
    """
    Kubernetes Info class
    """
    def __init__(self, match_labels: dict, target_service:str):
        self.match_labels = match_labels
        self.target_service = target_service

    def create_client(self):
        """
        Connect to Kubernetes API configuration
        """
        # Load Kubernetes configuration from default location
        try:
            config.load_kube_config()
        except Exception as error:
            print(f"Failed to load Kubernetes configs (Error: {error})")

        # Create Kubernetes client
        try:
            self.api_client = client.ApiClient()
        except Exception as error:
            print(f"Failed to initiate API client for Kubernetes (Error: {error})")

    def get_pod_name(self):
        """
        Get name of pod based on match_labels
        """
        namespace = ""
        label_selector = ",".join([f"{key}={value}" for key, value in self.match_labels.items()])
        core_v1_api = client.CoreV1Api(self.api_client)

        try:
            pod_list = core_v1_api.list_namespaced_pod(namespace, label_selector=label_selector)
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
            return False

        if not pod_list.items:
            print(f"{self.target_service} svc not found")
            return False

        pod = pod_list.items[0]
        return pod.metadata.name, pod.metadata.namespace

    def get_local_port(self, host:str='localhost', port:int=None):
        if port is None:
            for port in range(32768, 32901):
                try:
                    with socket.create_connection((host, port), timeout=1):
                        print(f"Local port {port} is not available.")
                except OSError:
                    print(f"Local port to be used for port forwarding : {port}")
                    return port

            print("Failed to find an available local port for port forwarding.")
            exit(1)
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"Local port {port} is not available.")
        except OSError:
            print(f"Local port to be used for port forwarding {self.pod_name}: {port}")
            return port


#-----------------------------------------------------------------------------------------------------------------------
# Declare Policy for KubeArmor
# :sample data:
#   {"Timestamp": "1703783776", "UpdatedTime": "2023-12-28T17:16:16.571714Z", "ClusterName": "default",
#     "HostName": "minikube", "NamespaceName": "default", "PodName": "nginx-7854ff8877-k4tsj",
#     "ContainerID": "cf3e3217059a56e21ca4cf676572ffb0aac66f0182fa107d239ce4636e53c396", "ContainerName": "nginx",
#     "HostPID": 1059919, "PPID": 1014073, "PID": 1673, "Type": "ContainerLog", "Operation": "Process",
#     "Resource": "/usr/bin/bash -c apt-get -y update && apt-get -y upgrade", "Data": "syscall=SYS_EXECVE",
#     "Result": "Passed", "ContainerImage": "nginx:latest@sha256:2bdc49f2f8ae8d8dc50ed00f2ee56d00385c6f8bc8a8b320d0a294d9e3b49026",
#     "ProcessName": "/usr/bin/bash", "HostPPID": 1059916, "Labels": "app=nginx",
#     "Owner": {"Ref": "Deployment", "Name": "nginx", "Namespace": "default"}}
#-----------------------------------------------------------------------------------------------------------------------

on error ignore

:set-params:
policy_name = kubearmor-system-policy
table_name = system_insight
if not !default_dbms then set default_dbms = kubearmor

is_policy = blockchain get policy where id = !policy_name
if !is_policy then goto end-script

<new_policy = {
    "mapping": {
        "id": !policy_name,,
        "dbms": !default_dbms,
        "table": !table_name,
        "readings": ""
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now()",
                "bring": "[UpdatedTime]"
            },
            "cluster_name": {
                "type": "string",
                "default": "default",
                "bring": "[ClusterName]"
            },
            "hostname_name": {
                "type": "string",
                "default": "minikube",
                "bring": "[HostName]"
            },
            "namespace": {
                "type": "string",
                "default": "default",
                "bring": "[NamespaceName]",
            },
            "pod_name": {
                "type": "string",
                "default": "",
                "bring": "[PodName]"
            },
            "container_id": {
                "type": "string",
                "default": "",
                "bring": "[ContainerID]"
            },
            "container_name": {
                "type": "string",
                "default": "",
                "bring": "[ContainerName]"
            },
            "host_pid": {
                "type": "int",
                "default": "",
                "bring": "[HostPID]"
            },
            "ppid": {
                "type": "int",
                "default": "",
                "bring": "[PPID]"
            },
            "pid": {
                "type": "int",
                "default": "",
                "bring": "[PID]"
            },
            "type": {
                "type": "string",
                "default": "",
                "bring": "[Type]"
            },
            "operation": {
                "type": "string",
                "default": "",
                "bring": "[Operation]"
            },
            "resource": {
                "type": "string",
                "default": "",
                "bring": "[Resource]"
            },
            "data": {
                "type": "string",
                "default": "",
                "bring": "[Data]"
            },
            "result": {
                "type": "string",
                "default": "",
                "bring": "[Result]"
            },
            "container_image": {
                "type": "string",
                "default": "",
                "bring": "[ContainerImage]"
            },
            "process_name": {
                "type": "string",
                "default": "",
                "bring": "[ProcessName]",
                "optional": true
            },
            "host_ppid": {
                "type": "string",
                "default": "",
                "bring": "[HostPPID]"
            },
            "labels": {
                "type": "string",
                "default": "",
                "bring": "[Labels]"
            },
            "owner_ref": {
                "type": "string",
                "default": "Deployment",
                "bring": "[Owner][Ref]"
            },
            "owner_name": {
                "type": "string",
                "default": "",
                "bring": "[Owner][Name]"
            },
            "owner_namespace": {
                "type": "string",
                "default": "default",
                "bring": "[Owner][Namespace]"
            },
            "source": {
                "type": "string",
                "default": "",
                "bring": "[Source]",
                "optional": true
            },
            "parent_process_name": {
                "type": "string",
                "default": "",
                "bring": "[ParentProcessName]",
                "optional": true
            },
            "uid": {
                "type": "int",
                "default": "",
                "bring": "[uid]",
                "optional": true
            }
        }
    }
}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!master_node











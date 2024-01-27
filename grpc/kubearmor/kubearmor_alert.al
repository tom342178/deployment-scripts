#-----------------------------------------------------------------------------------------------------------------------
# Declare Policy for KubeArmor
# :sample data:
#   {"Timestamp": "1703783776", "UpdatedTime": "2023-12-28T17:16:16.571714Z", "ClusterName": "default",
#     "HostName": "minikube", "NamespaceName": "default", "PodName": "nginx-7854ff8877-k4tsj",
#     "ContainerID": "cf3e3217059a56e21ca4cf676572ffb0aac66f0182fa107d239ce4636e53c396", "ContainerName": "nginx",
#     "HostPID": 1059919, "PPID": 1014073, "PID": 1673, "Type": "ContainerLog", "Operation": "Process",
#     "Resource": "/usr/bin/bash -c apt-get -y update && apt-get -y upgrade", "Data": "syscall=SYS_EXECVE",
#     "Result": "Passed",
#     "ContainerImage": "nginx:latest@sha256:2bdc49f2f8ae8d8dc50ed00f2ee56d00385c6f8bc8a8b320d0a294d9e3b49026",
#     "ProcessName": "/usr/bin/bash", "HostPPID": 1059916, "Labels": "app=nginx",
#     "Owner": {"Ref": "Deployment", "Name": "nginx", "Namespace": "default"}}
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/kubearmor_system_policy.al

on error ignore
:set-params:
new_policy = ""

:check-policy:
is_policy = blockchain get mapping where id = !grpc_name
if !is_policy then goto end-script


:prep-policy:
<new_policy = {
    "mapping": {
        "id": !grpc_name,
        "name": !grpc_name,
        "company": !company_name,
        "dbms": !default_dbms,
        "table": !grpc_response,
        "readings": "",
        "schema": {
            "timestamp": { # 1
                "type": "timestamp",
                "default": "now()",
                "apply" :  "epoch_to_datetime",
                "bring": "[Timestamp]"
            },
            "updated_timestamp": { # 2
                "type": "timestamp",
                "default": "now()",
                "bring": "[UpdatedTime]"
            },

            "cluster_name": { # 3
                "type": "string",
                "default": "",
                "bring": "[ClusterName]"
            },
            "hostname": { # 4
                "type": "string",
                "default": "",
                "bring": "[HostName]"
            },

            "namespace": { # 5
                "type": "string",
                "default": "",
                "bring": "[NamespaceName]"
            },
            "owner_ref": { # 31
                "type": "string",
                "default": "Deployment",
                "bring": "[Owner][Ref]"
            },
            "owner_name": { # 31
                "type": "string",
                "default": "",
                "bring": "[Owner][Name]"
            },
            "owner_namespace": { # 31
                "type": "string",
                "default": "",
                "bring": "[Owner][Namespace]"
            },
            "pod_name": { # 6
                "type": "string",
                "default": "",
                "bring": "[PodName]"
            },
            "labels": { #29
                "type": "string",
                "default": "",
                "bring": "[Labels]"
            },

            "container_id": { # 7
                "type": "string",
                "default": "",
                "bring": "[ContainerID]"
            },
            "container_name": { # 8
                "type": "string",
                "default": "",
                "bring": "[ContainerName]"
            },
            "container_image": { # 24
                "type": "string",
                "default": "",
                "bring": "[ContainerImage]"
            },

            "host_ppid": { # 27
                "type": "int",
                "default": "",
                "bring": "[HostPPID]"
            },
            "host_pid": { # 9
                "type": "int",
                "default": 0,
                "bring": "[HostPID]"
            },
            "ppid": { # 10
                "type": "int",
                "default": 0,
                "bring": "[PPID]"
            },
            "pid": { # 11
                "type": "int",
                "default": 0,
                "bring": "[PID]"
            },
            "uid": { # 12
                "type": "int",
                "default": 0,
                "bring": "[UID]"
            },

            "parent_process_name": {  # 25
                "type": "string",
                "default": "",
                "bring": "[ParentProcessName]"
            },
            "process_name": { # 26
                "type": "string",
                "default": "",
                "bring": "[ProcessName]",
                "optional": true
            },

            "policy_name": {
                "type": "string",
                "default": "",
                "bring": "[PolicyName]",
                "optional": "true"
            },
            "severity": {
                "type": "string",
                "default": "",
                "bring": "[Severity]",
                "optional": "true"
            },

            "tag": {
                "type": "string",
                "default": "",
                "bring": "[Tags]",
                "optional": "true"
            },
            "atag": {
                "type": "string",
                "default": "",
                "bring": "[ATags]",
                "optional": "true"
            },
            "message": {
                "type": "string",
                "default": "",
                "bring": "[Message]",
                "optional": "true"
            },

            "type": { # 17
                "type": "string",
                "default": "",
                "bring": "[Type]"
            },
            "source": { # 18
                "type": "string",
                "default": "",
                "bring": "[Source]"
            },
            "operation": { # 19
                "type": "string",
                "default": "",
                "bring": "[Operation]"
            },
            "resource": { # 20
                "type": "string",
                "default": "",
                "bring": "[Resource]",
                "apply" : "json_dump"
            },
            "data": { # 21
                "type": "string",
                "default": "",
                "bring": "[Data]"
            },

            "enforcer": {
                "type": "string",
                "default": "",
                "bring": "[Enforcer]",
                "optional": "true"
            },
            "action": {
                "type": "string",
                "default": "",
                "bring": "[Action]"
            },
            "result": { # 23
                "type": "string",
                "default": "",
                "bring": "[Result]"
            },
            "cwd": { # 32
                "type": "string",
                "default": "",
                "bring": "[CWD]"
            }
        }
    }
}>

:publish-policy:
process !local_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-    policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts




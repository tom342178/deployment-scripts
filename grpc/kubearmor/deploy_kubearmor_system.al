#-----------------------------------------------------------------------------------------------------------------------
# Deploy process to accept data from KubeArmor
# Steps:
#   1. Compile proto file
#   2. Set params
#   3. Declare Policy
#   4. gRPC client
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/deploy_kubearmor.al
on error ignore

# Compile proto file
#:compile-proto:
# on error goto compile-error
# compile proto where protocol_file=$ANYLOG_PATH/deployment-scripts/grpc/kubearmor/kubearmor/kubearmor.proto

# Set Params
:set-params:
grpc_name = system1
grpc_client_ip = 127.0.0.1
grpc_client_port = 50051
grpc_dir = $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/kubearmor/
grpc_proto = kubearmor
grpc_function = WatchLogs
grpc_request = RequestMessage
grpc_response = Log
grpc_service = LogService
grpc_value = (Filter = all)
grpc_limit = 0
set grpc_ingest = true
set grpc_debug = false

table_name = system_insight
if not !default_dbms then set default_dbms = kubearmor

:declare-policy:
process $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/kubearmor_system_policy.al


:run-grpc-client:
process $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/grpc_client.al


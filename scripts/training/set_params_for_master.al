#----------------------------------------------------------------------------------------------------------------------#
# Set parameters for AnyLog, specifically used for master node
# :required-params:
#   -> node_type
#   -> node_name
#   -> company_name
#   -> license_key
# :optional_params:
#   -> server and rest ports
#----------------------------------------------------------------------------------------------------------------------#

on error ignore

:set-configs:
set anylog_server_port = 32048
set anylog_rest_port = 32049

if $COMPANY_NAME then set company_name = $COMPANY_NAME
if $LICENSE_KEY then set license_key = $LICENSE_KEY

if $ANYLOG_SERVER_PORT then set anylog_server_port=$ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then set anylog_rest_port=$ANYLOG_REST_PORT

ledger_conn = !ip + : + !anylog_server_port

:end-script:
end script
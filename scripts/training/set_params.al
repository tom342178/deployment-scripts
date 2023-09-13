#-----------------------------------------------------------------------------------------------------------------------
# Based on docker-compose env file, set AnyLog parameters
# :required:
#   -> NODE_TYPE
#   -> NODE_NAME
#   -> LEDGER_CONN (except master)
# :first-time:
#   -> ANYLOG_SERVER_PORT
#   -> ANYLOG_REST_PORT
#   -> ANYLOG_BROKER_PORT (operator only)
#   -> LICNESE_KEY (master only)
#   -> COMPANY_NAME (master only)
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/set_params_blockchain.al

:set-params:
on error ignore
if $NODE_TYPE then set node_type = $NODE_TYPE
else node_type = generic
if $NODE_NAME then set node_name = $NODE_NAME
else goto missing-node-name

if !node_type == master then
do anylog_server_port=32048
do anylog_rest_port=32049
do ledger_conn = !ip + : + !anylog_server_port

if !node_type == query then
do anylog_server_port=32348
do anylog_rest_port=32349
do if not $LEDGER_CONN then goto ledger-conn-error

if !node_type == operator then
do anylog_server_port=32148
do anylog_rest_port=32149
do anylog_broker_port=32150
do if not $LEDGER_CONN then goto ledger-conn-error

if $LICENSE_KEY then license_key=$LICENSE_KEY
if $COMPANY_NAME then company_name = $COMPANY_NAME
if $LEDGER_CONN then ledger_conn=$LEDGER_CONN

if $ANYLOG_SERVER_PORT then anylog_server_port = $ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then anylog_rest_port = $ANYLOG_REST_PORT
if $ANYLOG_BROKER_PORT then anylog_broker_port = $ANYLOG_BROKER_PORT

:end-script:
end script

:terminate-scripts:
end scripts

:missing-node-name:
print "Missing node name, cannot continue..."
goto terminate-scripts

:ledger-conn-error:
print "Missing ledger connection information, cannot continue..."
goot terminate-scripts

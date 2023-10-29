#-----------------------------------------------------------------------------------------------------------------------
# Based on docker-compose env file, set AnyLog parameters
# :required:
#   -> NODE_TYPE
#   -> NODE_NAME
#   -> LEDGER_CONN (except master)
#   -> ENABLE_MQTT (operator only)
# :first-time:
#   -> ANYLOG_SERVER_PORT
#   -> ANYLOG_REST_PORT
#   -> ANYLOG_BROKER_PORT (operator only)
#   -> LICNESE_KEY (master only)
#   -> COMPANY_NAME (master only)
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/set_params_blockchain.al

on error ignore

:set-params:
on error ignore
if $NODE_TYPE then set node_type = $NODE_TYPE
else goto missing-node-type
if $NODE_NAME then set node_name = $NODE_NAME
else goto missing-node-name

if !node_type == master then
do anylog_server_port=32048
do anylog_rest_port=32049
do ledger_conn = !ip + : + !anylog_server_port

if !node_type == query then
do anylog_server_port=32348
do anylog_rest_port=32349

if !node_type == operator then
do anylog_server_port=32148
do anylog_rest_port=32149
do anylog_broker_port=32150

if $LICENSE_KEY then license_key=$LICENSE_KEY
else goto missing-license-key
if $COMPANY_NAME then company_name = $COMPANY_NAME
else goto missing-company-name
if $LEDGER_CONN then ledger_conn=$LEDGER_CONN
else goto missing-ledger-conn

if $ANYLOG_SERVER_PORT then anylog_server_port = $ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then anylog_rest_port = $ANYLOG_REST_PORT
if $ANYLOG_BROKER_PORT then anylog_broker_port = $ANYLOG_BROKER_PORT

set enable_mqtt = false
if $ENABLE_MQTT == true or $ENABLE_MQTT == True or $ENABLE_MQTT == TRUE then set enable_mqtt = true

cluster_name = !node_name.name + -cluster
default_dbms = !company_name.name

#if $CLUSTER_NAME then cluster_name = $CLUSTER_NAME
#if $DEFAULT_DBMS then default_dbms = $DEFAULT_DBMS


:end-script:
end script

:terminate-scripts:
exit scripts

:missing-node-type:
print "Missing node type, cannot continue..."
goto terminate-scripts

:missing-license-key:
print "Missing license key, cannot continue..."
goto terminate-scripts

:missing-company-name:
print "Missing company name, cannot continue..."
goto terminate-scripts

:missing-node-name:
print "Missing node name, cannot continue..."
goto terminate-scripts

:missing-ledger-conn:
print "Missing ledger connection information, cannot continue..."
goto terminate-scripts


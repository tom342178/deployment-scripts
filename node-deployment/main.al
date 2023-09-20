#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an AnyLog instance based on user configurations
# If !policy_based_networking == true, the deployment is executed in the following way
# Script: !local_scripts/start_node_policy_based.al
#   1. set params
#   2. run tcp server
#   3. blockchain seed
#   4. config policy
#-----------------------------------------------------------------------------------------------------------------------
# python3.10 AnyLog-Network/source/anylog.py process $ANYLOG_PATH/deployment-scripts/node-deployment/main.al

:set-configs:
on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $ANYLOG_ID_DIR then set id_dir = $ANYLOG_ID_DIR

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

create work directories

:set-params:
process !local_scripts/set_params.al
process !local_scripts/run_tcp_server.al

:create-database:
if !node_type == master then process !local_scripts/database/configure_dbms_blockchain.al

:blockchain-seed:
on error goto blockchain-seed-error
if !ledger_conn and !node_type != master then blockchain seed from !ledger_conn
wait 5

:blockchain-get:
on error ignore
master_policy = blockchain get master
if !master_policy then
do set debug on
do if not !license_key then license_key = from !master_policy bring [*][license]
do ledger_conn = from !master_policy bring.ip_port
do print !license_key
do print !ledger_conn
do set deug off

:declare-policy:
process !local_scripts/policies/config_policy.al

:execute-license:
on error call license-error
set license where activation_key = !license_key

:end-script:
end script

:blockchain-seed-error:
print "Failed to run blockchain seed"
goto end-script

:license-key-error:
print "Failed to enable license key"
return

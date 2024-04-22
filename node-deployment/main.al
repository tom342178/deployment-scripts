#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an AnyLog instance based on user configurations
# If !policy_based_networking == true, the deployment is executed in the following way
# Script: !local_scripts/start_node_policy_based.al
#   1. set params
#   2. run tcp server
#   3. blockchain seed
#   4. config policy
#-----------------------------------------------------------------------------------------------------------------------
# python3.10 AnyLog-Network/edge_lake/anylog.py process $ANYLOG_PATH/deployment-scripts/node-deployment/main.al

:set-configs:
on error ignore
set debug off
set echo queue on
set authentication off

:directories:
set anylog_path = /app
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH

set anylog home !anylog_path
wait 1
get dictionary _dir
create work directories

set local_scripts = /app/deployment-scripts/node-deployment
set test_dir = /app/deployment-scripts/test
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

:set-params:
process !local_scripts/set_params.al
process !local_scripts/run_tcp_server.al

:blockchain-seed:
on error call blockchain-seed-error
if !node_type != master then
do blockchain seed from !ledger_conn
do wait 10

:declare-policy:
process !local_scripts/policies/config_policy.al

:set-license:
on error ignore
master_license = blockchain get master bring [*][license]
on error goto license-error
if !license_key then set license where activation_key = !license_key
if not !license_key and !master_license then set license where activation_key = !master_license
if not !license_key and not !master_license then goto license-error

:end-script:
get processes
if !enable_mqtt == true then get msg client
end script

:blockchain-seed-error:
print "Failed to run blockchain seed"
return

:license-error:
print "Failed set license"
goto end-script


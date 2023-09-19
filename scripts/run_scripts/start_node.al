#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an AnyLog instance based on user configurations
# If !policy_based_networking == true, the deployment is executed in the following way
# Script: !local_scripts/start_node_policy_based.al
#    1. set params
#    2. declare policy (if DNE)
#    3. connect to network based on policy
#    4. (REST) authentication
#    5. specific configs for node <-- we won’t declare a policy here any longer
#    5. MQTT
#    6. local  scripts
#-----------------------------------------------------------------------------------------------------------------------
# python3.10 AnyLog-Network/source/anylog.py process deployment-scripts/scripts/run_scripts/start_node.al

:enable-cli:
set enable_cli = true
if $ENABLE_CLI == false or $ENABLE_CLI == False or $ENABLE_CLI == FALSE then set enable_cli = false

on error call enable-cli-error
if !enable_cli == false then set cli off

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
process !local_scripts/deployment_scripts/set_params.al
process !local_scripts/deployment_scripts/run_tcp_server.al

:blockchain-seed:
reset error log
on error goto blockchain-seed-error
blockchain seed from !ledger_conn

:get-license:
on error ignore
master_policy = blockchain get master
if !master_policy then
do license_key = from !master_policy bring [master][license]
do ledger_conn = from !master_policy bring.ip_port

:execute-license:
on error call license-error
set license where activation_key=!license_key


:end-script:
end script:

:blockchain-seed-error:
print "Failed to run blockchain seed"
goto end-script

:license-key-error:
print "Failed to enable license key"
return

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

:set-configs:
on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $ANYLOG_ID_DIR then set id_dir = $ANYLOG_ID_DIR

if $BLOCKCHAIN_DIR then
do set blockchain_dir = $BLOCKCHAIN_DIR
do set blockchain_file = !blockchain_dir/blockchain.json
do set blockchain_new = !blockchain_dir/blockchain.new
do set blockchain_sql = !blockchain_dir/blockchain/blockchain.sql

if $DATA_DIR then  # default: /app/AnyLog-Network/data
do set data_dir = $DATA_DIR
do set archive_dir = !data_dir/archive
do set bkup_dir = !data_dir/bkup
do set blobs_dir = !data_dir/blobs
do set bwatch_dir = !data_dir/bwatch
do set dbms_dir = !data_dir/dbms
do set distr_dir = !data_dir/distr
do set err_dir = !data_dir/error
do set pem_dir = !data_dir/pem
do set prep_dir = !data_dir/prep
do set test_dir = !data_dir/test
do set tmp_dir = !data_dir/tmp
do set watch_dir = !data_dir/watch

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

create work directories

:set-params:
process !local_scripts/deployment_scripts/set_params.al
if $NODE_TYPE == none then goto set-license

:networking-configs:
# set basic configurations
# --> TCP
# --> REST
# --> Broker (if set)
if !policy_based_networking == true then process !local_scripts/deployment_scripts/policies/network_config_policy.al
else process !local_scripts/deployment_scripts/network_configs.al


:declare-policies:
process !local_scripts/deployment_scripts/declare_policies.al


:set-rest-authentication:
if !enable_rest_auth == true then process !local_scripts/deployment_scripts/authentication/basic_rest_authentication.al

if $NODE_TYPE == rest then goto set-license

:set-authentication:
if !enable_auth == true then
do set authentication on
do process !local_scripts/deployment_scripts/authentication/node_keys.al

:node-specific-scripts:
if !deploy_ledger == true then process !local_scripts/run_scripts/start_master.al
if !deploy_operator == true  then process !local_scripts/run_scripts/start_operator.al
if !deploy_publisher == true then process !local_scripts/run_scripts/start_publisher.al
if !deploy_query == true then process !local_scripts/run_scripts/start_query.al

:other-scripts:
if !enable_mqtt == true then process !local_scripts/sample_code/basic_mqtt_process.al

if !deploy_local_script == true then
do is_file = file test !local_scripts/deployment_scripts/local_script.al
do if !is_file == true then process !local_scripts/deployment_scripts/local_script.al

if !monitor_nodes == true then process !local_scripts/deployment_scripts/policies/monitoring_node_policy.al

:set-license:
on error call license-key-error
set license where activation_key = !license_key

:end-script:
end script

:license-key-error:
print "Failed to set license key"
return

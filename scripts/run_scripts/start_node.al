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
# python3.9 AnyLog-Network/source/cmd/user_cmd.pyc process /app/AnyLog-Network/scripts/run_scripts/start_node.al

:set-configs:
on error ignore
set debug off
set authentication off
set echo queue on

if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
create work directories

system mv $ANYLOG_PATH/AnyLog-Network/test $ANYLOG_PATH/AnyLog-Network/data

:set-params:
process !local_scripts/deployment_scripts/set_params.al

:set-license:
on error call license-key-error
set license where activation_key = !license_key

if $NODE_TYPE == none then goto end-script

:declare-policies:
if !config_policy == true  then process !local_scripts/deployment_scripts/declare_policies.al

:networking-configs:
# set basic configurations
# --> TCP
# --> REST
# --> Broker (if set)
process !local_scripts/deployment_scripts/network_configs.al

:set-rest-authentication:
if !enable_rest_auth == true then process !local_scripts/deployment_scripts/authentication/basic_rest_authentication.al

if $NODE_TYPE == rest then goto end-script

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

#process !local_scripts/sample_code/monitoring_node_policy.al

:end-script:
end script

:license-key-error:
print "Failed to set license key"
return

on error ignore
:check-policy:
policy_id = blockchain get config where name = !config_name and node_type=!node_type and company=!company_name bring [*][id]
if !policy_id then goto end-script
if not !policy_id and !create_policy == true then goto declare-policy-error

:declare-base:
set policy new_policy [config] = {}

set policy new_policy [config][name] = !config_name
set policy new_policy [config][node_type] = !node_type
set policy new_policy [config][company] = !company_name

:network-configs:
if !overlay_ip and !tcp_bind == true then set policy new_policy [config][ip] = '!overlay_ip'
if not !overlay_ip and !tcp_bind == true then set policy new_policy [config][ip] = '!ip'
if !tcp_bind == false then
do set policy new_policy [config][ip] = '!external_ip'
do set policy new_policy [config][internal_ip] = '!ip'

if !overlay_ip and !rest_bind == true then  policy new_policy [config][rest_ip] = '!overlay_ip'
if not !overlay_ip and !rest_bind == true then set policy new_policy [config][rest_ip] = '!ip'
if !anylog_broker_port and !overlay_ip and !broker_bind == true then set policy new_policy [config][broker_ip] = '!overlay_ip'
if !anylog_broker_port and not !overlay_ip and !broker_bind == true then set policy new_policy [config][broker_ip] = '!ip'

set policy new_policy [config][port] = '!anylog_server_port.int'
set policy new_policy [config][rest_port] = '!anylog_rest_port.int'
if !anylog_broker_port then set policy new_policy[config][broker_port] = '!anylog_broker_port.int'

set policy new_policy [config][threads] = '!tcp_threads.int'
set policy new_policy [config][rest_threads] = '!rest_threads.int'
set policy new_policy [config][rest_timeout] = '!rest_timeout.int'
if !anylog_broker_port then set policy new_policy [config][broker_threads] = '!broker_threads.int'

:scripts:
#----------------------------------------------------------------------------------------------------------------------#
# scripts
#   --> run scheduler
#   --> blockchain_sync
#   --> declare policy
#   --> connect database(s)
#   --> run operator || publisher
#   --> run monitoring
#   --> run mqtt client
#   --> ru personalized script
#----------------------------------------------------------------------------------------------------------------------#
#set policy new_policy [config][scripts] = [
    "run scheduler 1",
    "do run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn",
#    "if !node_type == master then process !local_scripts/deployment_scripts_new/database/configure_dbms_blockchain.al",
#    "if !deploy_system_query == true then process !local_scripts/deployment_scripts_new/database/configure_dbms_system_query.al",
#    "if !node_type == operator then process !local_scripts/deployment_scripts_new/database/configure_dbms_system_query.al",
#    "if !node_type == operator then process !local_scripts/deployment_scripts_new/database/configure_dbms_system_query.al",
#    "if !enable_nosql == true then process !local_scripts/deployment_scripts_new/database/configure_dbms_nosql.al",
#    "if !node_type == operator or !node_type == publisher then process !local_scripts/deployment_scripts_new/database/configure_dbms_almgm.al",
#]

:publish-policy:
process !local_scripts/deployment_scripts_new/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error
set create_policy = true
goto check-policy

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign configuration policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare configuration policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare configuration policy on blockchain"
goto terminate-scripts


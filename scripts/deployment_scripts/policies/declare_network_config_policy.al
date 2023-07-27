#-----------------------------------------------------------------------------------------------------------------------
# Create & execute policy for networking
#
# ---- Sample Policy ---
#   {"config": {
#       "name": !config_policy_name,
#       "company": !company_name,
#       "ip": !external_ip,
#       "local_ip": !ip,
#       "port": !anylog_server_port,
#       "rest_port": !anylog_rest_port,
#       "broker_port": !anylog_broker_port
#   }}
# ---- Sample Policy ---
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/declare_network_config_policy.al

on error ignore
i = 0

:check-policy:
policy_id = blockchain get config where name=!config_policy_name and company=!company_name bring.first [*][id]
if !is_policy then goto run-policy

:declare-config:
on error ignore
set policy new_policy [config] = {}

set policy new_policy [config][name] = !config_policy_name
set policy new_policy [config][company] = !company_name

:tcp-info:
# if one of the default IPs is missing or the TCP port then we cannot continue
if not !anylog_server_port or not !external_ip or not !ip then goto goto tcp-info-error

if !tcp_bind == false then
do set policy new_policy [config][ip] = '!external_ip'
do set policy new_policy [config][local_ip] = '!ip'
do set policy new_policy [config][port] = '!anylog_server_port.int'
do set policy new_policy [config][local_port] = '!anylog_server_port.int'

if !tcp_bind == true then
do set policy new_policy [config][ip] = '!ip'
do set policy new_policy [config][port] = '!anylog_server_port.int'

:rest-info:
if not !anylog_rest_port then goto rest-info-message
if !rest_bind == true then set policy new_policy [config][rest_ip] = '!ip'
set policy new_policy [config][rest_port] = '!anylog_rest_port.int'

:broker-info:
if not !anylog_broker_port then goto validate-policy

if broker_bind == true then set policy new_policy [config][broker_ip] = '!ip'
set policy new_policy [config][broker_port] = '!anylog_broker_port.int'

:validate-policy:
on error goto validate-policy-error
test_policy = json !new_policy
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

on error ignore
policy_id = blockchain get config where name=!config_policy_name and company=!company_name bring.first [*][id]

:run-policy:
on error goto run-policy-error
if not !policy_id then go missing-policy-id
config from policy where id = !policy_id

:end-script:
end script

:terminate-scripts:
exit scripts

:tcp-info-error:
if not !anylog_server_port then echo 'Error: Missing TCP port information, cannot continue'
if not !external_ip or not !ip then echo 'Error: Missing external and/or local IP address. Cannot continue'
goto terminate-scripts


:rest-info-message:
echo 'Notice: missing REST information'
goto broker-info

:sign-policy-error:
echo "Error: Failed to sign cluster policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with cluster policy declaration"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for " !policy_type
return

:config-policy-error:
echo "Failed to configure node base on policy ID: " !policy_id
goto terminate-scripts

:missing-policy-id:
echo "Unable to locate policy for network configuration."
goto end-script

:run-policy-error:
echo "Error: failed to run process from policy"
goto end-script







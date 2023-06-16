#-----------------------------------------------------------------------------------------------------------------------
# Create & execute policy for networking
#
# ---- Sample Policy ---
#   {"config": {
#       "name": !network_config_policy_name,
#       "company": !company_name,
#       "ip": !external_ip,
#       "local_ip": !ip,
#       "port": !anylog_server_port,
#       "rest_port": !anylog_rest_port,
#       "broker_port": !anylog_broker_port
#   }}
# ---- Sample Policy ---
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/network_config_policy.al

on error ignore
i = 0

:check-policy:
policy_id = blockchain get config where name=!network_config_policy_name and company=!company_name bring.first [*][id]
if !is_policy then
do on error config-policy-error
do config from policy where id = !policy_id
do goto deploy-policy
else if i == 1 then goto no-policy-error

set policy new_policy [config] = {}

set policy new_policy [config][name] = !network_config_policy_name
set policy new_policy [config][company] = !company_name

:tcp-info:
# if one of the default IPs is missing or the TCP port then we cannot continue
if not !anylog_server_port or not !external_ip or not !ip then goto goto tcp-info-error

set policy new_policy [config][port] = '!anylog_server_port.int'
if !tcp_bind == false then
do set policy new_policy [config][ip] = '!external_ip'
do set policy new_policy [config][local_ip] = '!ip'
else if !tcp_bind == true then set policy new_policy [config][ip] = '!ip'

:rest-info:
if not !anylog_rest_port then goto rest-info-message
if !rest_bind == true then set policy new_policy [config][rest_ip] = '!ip'
set policy new_policy [config][rest_port] = '!anylog_rest_port.int'

:broker-info:
if not !anylog_broker_port then goto end-script

if broker_bind == true then set policy new_policy [config][broker_ip] = '!ip'
set policy new_policy [config][broker_port] = '!anylog_broker_port.int'

:declare-policy:
process !local_scripts/deployment_scripts/policies/declare_policy.al
i = 1
goto check-policy

:end-script:
end script

:terminate-scripts:
exit scripts

:config-policy-error:
echo "Failed to configure node base on policy ID: " !policy_id
goto terminate-scripts

:tcp-info-error:
if not !anylog_server_port then echo 'Error: Missing TCP port information, cannot continue'
if not !external_ip or not !ip then echo 'Error: Missing external and/or local IP address. Cannot continue'
goto terminate-scripts


:rest-info-message:
echo 'Notice: missing REST information'
goto broker-info






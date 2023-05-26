#-----------------------------------------------------------------------------------------------------------------------
# Based on the given configuration file create a generic network configuration policy. Unlike a node policy, the values
# are variable names, thus the same policy can be executed on node with different IP and port information.
#
# The name of the policy is either set by the user in the configurations, or is based on the node_type
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/prepare_config_policy.al

on error ignore

:prep-policy:
set policy new_policy [config] = {}

set policy new_policy [config][name] = !config_policy_name
if !company_name then set policy new_policy [config][company] = !company_name

:tcp-info:
# if one of the default IPs is missing or the TCP port then we cannot continue
if not !anylog_server_port or not !external_ip or not !ip then goto goto tcp-info-error

set policy new_policy [config][port] = '!anylog_server_port.int'
if !tcp_bind == false then
do set policy new_policy [config][ip] = '!external_ip'
do set policy new_policy [config][local_ip] = '!ip'
else if !tcp_bind == true
do set policy new_policy [config][ip] = '!ip'

:rest-info:
if not !anylog_rest_port then goto rest-info-message

set policy new_policy [config][rest_port] = '!anylog_rest_port.int'

if !rest_bind == true then
do set policy new_policy [config][rest_ip] = !ip

:broker-info:
if not !anylog_broker_port then goto end-script

set policy new_policy [config][broker_port] = '!anylog_broker_port.int'

if !broker_bind == true then
do set policy new_policy [config][broker_ip] = '!ip'

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

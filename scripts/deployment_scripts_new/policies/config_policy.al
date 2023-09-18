:declare-base:
config_name = !node_type.name + - + !company_name.name + -configs
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

set policy new_policy [config][port] = '!anylog_server_port'
set policy new_policy [config][rest_port] = '!anylog_rest_port'
if !anylog_broker_port then set policy new_policy[config][broker_port] = '!anylog_broker_port'

set policy new_policy [config][tcp_threads] = '!tcp_threads'
set policy new_policy [config][rest_threads] = '!rest_threads'
set policy new_policy [config][rest_timeout] = '!rest_timeout'
if !anylog_broker_port then set policy new_policy [config][broker_threads] = '!broker_threads'

:publish-policy:
process !local_scripts/training/generic_policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

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


#-----------------------------------------------------------------------------------------------------------------------
# Code to generate policy based on user input, for node of type:
#   - master
#   - operator
#   - publisher
#   - query
#
# The values set into the policy are hard coded, meaning they use the actual values in the Anylog dictionary. If you'd
# like to use variable names for network connectivity, rather than actual values, then a config policy might be better
# suited. To execute a config policy: process !local_scripts/deployment_scripts/policies/declare_config_policy.al
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/prepare_node_policy.al


on error ignore
:general-info:
# declare policy
set policy new_policy [!policy_type] = {}

# basic information
if !node_name then set policy new_policy [!policy_type][name] = !node_name
if !company_name then set policy new_policy [!policy_type][company] = !company_name
if !hostname then set policy new_policy [!policy_type][hostname] = !hostname
if !loc then set policy new_policy [!policy_type][loc] = !loc
if !country then set policy new_policy [!policy_type][country] = !country
if !state then set policy new_policy [!policy_type][state] = !state
if !city then set policy new_policy [!policy_type][city] = !city

:tcp-info:
# if one of the default IPs is missing or the TCP port then we cannot continue
if not !anylog_server_port or not !external_ip or not !ip then goto goto tcp-info-error

set policy new_policy [!policy_type][port] = !anylog_server_port.int

if !tcp_bind == false then
do set policy new_policy [!policy_type][ip] = !external_ip
do set policy new_policy [!policy_type][local_ip] = !ip

if !tcp_bind == false and !kubernetes_service_ip then set policy new_policy [!policy_type][local_ip] = !kubernetes_service_ip
if !tcp_bind == false and !overlay_ip and not !kubernetes_service_ip then set policy new_policy [!policy_type][local_ip] = !overlay_ip

if !tcp_bind == true then
do set policy new_policy [!policy_type][external_ip] = !external_ip
do set policy new_policy [!policy_type][ip] = !ip

if !tcp_bind == true and !kubernetes_service_ip then set policy new_policy [!policy_type][ip] = !kubernetes_service_ip
if !tcp_bind == true and !overlay_ip  and not !kubernetes_service_ip then set policy new_policy [!policy_type][ip] = !overlay_ip

if !proxy_ip then set policy new_policy [!policy_type][proxy_ip] = !proxy_ip

# if overlay with Kubernetes - then use overlay as external IP
if !kubernetes_service_ip and !overlay_ip then
do if !tcp_bind == false then set policy new_policy [!policy_type][ip] = !overlay_ip
do if !tcp_bind == true then set policy new_policy [!policy_type][external_ip] = !overlay_ip

:rest-info:
if not !anylog_rest_port then goto rest-info-message

set policy new_policy [!policy_type][rest_port] = !anylog_rest_port.int

if !rest_bind == true then set policy new_policy [!policy_type][rest_ip] = !ip
if !rest_bind == true and !kubernetes_service_ip then set policy new_policy [!policy_type][rest_ip] = !kubernetes_service_ip
if !rest_bind == true and !overlay_ip then set policy new_policy [!policy_type][rest_ip] = !overlay_ip

:broker-info:
if not !anylog_broker_port then goto operator-configs

set policy new_policy [!policy_type][broker_port] = !anylog_broker_port.int

if !broker_bind == true then set policy new_policy [!policy_type][broker_ip] = !ip
if !broker_bind == true and !kubernetes_service_ip then set policy new_policy [!policy_type][broker_ip] = !kubernetes_service_ip
if !broker_bind == true and !overlay_ip then set policy new_policy [!policy_type][broker_ip] = !overlay_ip

:operator-configs:
if !policy_type != operator then goto end-script

if not !cluster_id then goto cluster-info-error
else set policy new_policy [!policy_type][cluster] = !cluster_id
if !member then set policy new_policy [!policy_type][member] = !member.int

if !enable_partitions == false then goto end-script
<set policy new_policy [!policy_type][script] = [
    'partition !default_dbms !table_name using !partition_column by !partition_interval',
    'schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep'
]>

:end-script:
end script

:terminate-scripts:
exit scripts

:tcp-info-error:
if not !anylog_server_port then echo "Error: Missing TCP port information, cannot continue"
if not !external_ip or not !ip then echo "Error: Missing external and/or local IP address. Cannot continue"
goto terminate-scripts

:rest-info-message:
echo "Notice: missing REST information"
goto broker-info

:cluster-info-error:
echo "Error: Missing cluster information for operator. Cannot declare policy"
goto terminate-scripts



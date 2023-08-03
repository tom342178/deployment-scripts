#-----------------------------------------------------------------------------------------------------------------------
# 1. Check if policy exists based on name and company if so echo error and end script
# 2. Extend step 1 and include IP addresses based on binding as well as TCP and REST port
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/validate_node_policy.al


<is_policy = blockchain get !policy_type where
    name=!node_name and company=!company_name>

if !is_policy then
do echo A policy for !policy_type named !node_name for !company_name already exists
do goto end-script

if !overlay_ip then goto generic-ip-networking
:check-node-policy:
if !tcp_bind == true and not !overlay_ip then
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!ip and
    port=!anylog_server_port and
    rest=!anylog_rest_port>

if !tcp_bind == true and !overlay_ip then
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!overlay_ip and
    port=!anylog_server_port and
    rest=!anylog_rest_port>

if !tcp_bind == false and not !overlay_ip then
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!external_ip and
    local_ip=!ip and
    port=!anylog_server_port and
    rest=!anylog_rest_port>

if !tcp_bind == false and not !overlay_ip then
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!external_ip and
    local_ip=!overlay_ip and
    port=!anylog_server_port and
    rest=!anylog_rest_port>
 
:end-script: 
end script 

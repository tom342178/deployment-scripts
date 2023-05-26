#-----------------------------------------------------------------------------------------------------------------------
# If !policy_based_networking == true - check whether a policy exists based on name + company only
# If !policy_based_networking == false then
#   1. check if a policy of a given type with the given parameters provided exists
#   2. if not, check if a policy of the same type with the same name and company exists
#       - if so write notice and terminate process
#       - if not continue
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/validate_node_policy.al


if not !overlay_ip then goto generic-ip-networking
 
:overlay-ip-networking: 
if not !is_policy and !overlay_ip and !tcp_bind == true and !anylog_broker_port then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!overlay_ip and port=!anylog_server_port and
    rest_port=!anylog_rest_port and
    broker_port=!anylog_broker_port
>
if not !is_policy and !overlay_ip and !tcp_bind == false and !anylog_broker_port then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!overlay_ip and
    local_ip=!overlay_ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port and
    broker_port=!anylog_broker_port
> 
if not !is_policy and !overlay_ip and !tcp_bind == true then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!overlay_ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port
>
if not !is_policy and !overlay_ip and !tcp_bind == false then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!overlay_ip and
    local_ip=!overlay_ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port
> 
 
if not !is_policy and !policy then goto end-script 
 
:generic-ip-networking: 
if not !is_policy and !tcp_bind == true and !anylog_broker_port then 
<do is_policy = blockchain get !policy_type where 
    name=!node_name and  
    company=!company_name and  
    ip=!ip and  
    port=!anylog_server_port and  
    rest_port=!anylog_rest_port and  
    broker_port=!anylog_broker_port 
> 
if not !is_policy and !tcp_bind == false and !anylog_broker_port then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!external_ip and
    local_ip=!ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port and
    broker_port=!anylog_broker_port
> 
if not !is_policy and !tcp_bind == true then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port
> 
if not !is_policy and !tcp_bind == false then 
<do is_policy = blockchain get !policy_type where
    name=!node_name and
    company=!company_name and
    ip=!external_ip and
    local_ip=!ip and
    port=!anylog_server_port and
    rest_port=!anylog_rest_port
>
 
:end-script: 
end script 

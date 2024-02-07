#-----------------------------------------------------------------------------------------------------------------------
# Validate if policy exists
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/policies/validate_policy.al


if !node_type != operator then goto generic-node-validate
:operator-node-validator:
if !tcp_bind == false then
<do is_policy = blockchain get operator where
    company=!company_name and
    name=!node_name and
    cluster=!cluster_id and
    ip = !external_ip and
    port = !anylog_server_port>
if !tcp_bind == true and !overlay_ip then
<do is_policy = blockchain get operator where
    company=!company_name and
    name=!node_name and
    cluster=!cluster_id and
    ip = !overlay_ip and
    port = !anylog_server_port>
if !tcp_bind == true and not !overlay_ip then
<do is_policy = blockchain get operator where
    company=!company_name and
    name=!node_name and
    cluster=!cluster_id and
    ip = !ip and
    port = !anylog_server_port>


goto end-script

:generic-node-validate:
if !tcp_bind == false then
<do is_policy = blockchain get !node_type where
    company=!company_name and
    name=!node_name and
    ip = !external_ip and
    port = !anylog_server_port>
if !tcp_bind == true and !overlay_ip then
<do is_policy = blockchain get !node_type where
    company=!company_name and
    name=!node_name and
    ip = !overlay_ip and
    port = !anylog_server_port>
if !tcp_bind == true and not !overlay_ip then
<do is_policy = blockchain get !node_type where
    company=!company_name and
    name=!node_name and
    ip = !ip and
    port = !anylog_server_port>

:end-script:
end script

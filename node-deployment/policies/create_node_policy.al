#----------------------------------------------------------------------------------------------------------------------#
# Create policy for master, query or publisher
#   --> check if policy exists
#   --> prepare policy
#   --> declare policy
#   --> recheck
# :sample-policy:
#   {"master": {
#       "name": "anylog-master",
#       "company": "AnyLog Co.",
#       "ip": "136.23.47.189",
#       "local_ip": "136.23.47.189",
#       "port": 32048,
#       "rest_port": 32049,
#       "loc": "37.425423, -122.078360",
#       "country": "US",
#       "state": "CA",
#       "city": "Mountain View"
#   }}
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/policies/create_node_policy.al

on error ignore
set create_policy = false

:check-policy:
process !local_scripts/policies/validate_policy.al

if not !is_policy and !create_policy == false then goto create-policy
if not !is_policy and !create_policy == true then goto config-policy-error
if !is_policy and !node_type != operator then goto end-script
if !is_policy and !node_type == operator then goto operator-info

:create-policy:
set new_policy = ""
set policy new_policy [!node_type] = {}
set policy new_policy [!node_type][name] = !node_name
set policy new_policy [!node_type][company] = !company_name

:network-master:
set policy new_policy [!node_type][ip] = !external_ip
else if !tcp_bind == true  and !overlay_ip then set policy new_policy [!node_type][ip] = !overlay_ip
else if !tcp_bind == false and !overlay_ip then set policy new_policy [!node_type][local_ip] = !overlay_ip
else set policy new_policy [!node_type][local_ip] = !ip

if !rest_bind == true and !overlay_ip then set policy new_policy [!node_type][rest_ip] = !overlay_ip
if !rest_bind == true and not !overlay_ip then set policy new_policy [!node_type][rest_ip] = !ip

if !broker_bind == true and !overlay_ip then set policy new_policy [!node_type][broker_ip] = !overlay_ip
else if !broker_bind == true and not !overlay_ip then set policy new_policy [!node_type][broker_ip] = !ip

set policy new_policy [!node_type][port] = !anylog_server_port.int
set policy new_policy [!node_type][rest_port] = !anylog_rest_port.int
if !anylog_broker_port then set policy new_policy [!node_type][broker_port] = !anylog_broker_port.int

if !node_type == operator then goto set-cluster
else if !node_type != master then goto set-location

:set-license:
if !node_type == master and !license_key then set policy new_policy [!node_type][license] = !license_key
goto set-location

:set-cluster:
if not !cluster_id then cluster_id = blockchain get cluster where name=!cluster_name and company=!company_name bring.first [*][id]
if not !cluster_id then goto missing-cluster-error
else set policy new_policy [!node_type][cluster] = !cluster_id

:set-location:
if !loc then set policy new_policy [!node_type][loc] = !loc
if !country then set policy new_policy [!node_type][country] = !country
if !state then set policy new_policy [!node_type][state] = !state
if !city then set policy new_policy [!node_type][city] = !city

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_policy = true
goto check-policy

:operator-info:
on error ignore
operator_id = from !is_policy bring.last [*][id]
if not !operator_id then goto config-policy-error


:end-script:
end script

:terminate-scripts:
exit scripts

:ip-error:
print "A node policy with the same company and node name already exists under a different IP address: " !ip_address
goto terminate-scripts

:missing-cluster-error:
print "Unable to create operator policy, missing cluster ID information"
goto terminate-scripts

:sign-policy-error:
print "Failed to sign master policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member master policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare master policy on blockchain"
goto terminate-scripts

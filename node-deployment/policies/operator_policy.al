#----------------------------------------------------------------------------------------------------------------------#
# Create policy for operator
#   --> check if policy exists
#   --> prepare policy
#   --> declare policy
#   --> recheck
# :sample-policy:
#   {"operator": {
#       "name": "anylog-operator",
#       "company": "AnyLog Co.",
#       "ip": "136.23.47.189",
#       "local_ip": "136.23.47.189",
#       "port": 32248,
#       "rest_port": 32249,
#       "cluster": "",
#       "loc": "37.425423, -122.078360",
#       "country": "US",
#       "state": "CA",
#       "city": "Mountain View",
#       "script": [ // validate only if data partitioning is initially enabled
#           "partition !default_dbms !table_name using !partition_column by !partition_interval",
#           "schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep"
#       ]
#   }}
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/policies/operator_policy.al

on error ignore
set create_policy = false

:check-policy:
process !local_scripts/policies/validate_policy.al

if not !is_policy then goto create-policy
if !is_policy then
do ip_address = from !is_policy bring [*][ip]
do if !ip_address != !external_ip and !ip_address != !ip and !ip_address != !overlay_ip then goto ip-error
do operator_id = from !is_policy bring [*][id]

if !operator_id then goto config-policy
if not !operator_id and !create_policy == true then goto declare-policy-error

:create-policy:
set new_policy = ""
set policy new_policy [operator] = {}
set policy new_policy [operator][name] = !node_name
set policy new_policy [operator][company] = !company_name

:network-operator:
set policy new_policy [operator][ip] = !external_ip
set policy new_policy [operator][local_ip] = !ip
if !tcp_bind == false and !overlay_ip then set policy new_policy [operator][local_ip] = !overlay_ip
else if !tcp_bind == true and !overlay_ip then set policy new_policy [operator][ip] = !overlay_ip
else if !tcp_bind == true and not !overlay_ip then set policy new_policy [operator][ip] = !ip

if !rest_bind == true and !overlay_ip then set policy new_policy [operator][rest_ip] = !overlay_ip
else if !rest_bind and not !overlay_ip then set policy new_policy [operator][rest_ip] = !ip

if !broker_bind == true and !overlay_ip then set policy new_policy [operator][rest_ip] = !overlay_ip
else if !broker_bind == true and not !overlay_ip then set policy new_policy [operator][rest_ip] = !ip

if !proxy_ip then set policy new_policy[operator][proxy] = !proxy_ip

set policy new_policy [operator][port] = !anylog_server_port.int
set policy new_policy [operator][rest_port] = !anylog_rest_port.int
if !anylog_broker_port then set policy new_policy [operator][broker_port] = !anylog_broker_port.int

:cluster-info:
if !cluster_id then set policy new_policy [operator][cluster] = !cluster_id

:location:
if !loc then set policy new_policy [operator][loc] = !loc
if !country then set policy new_policy [operator][country] = !country
if !state then set policy new_policy [operator][state] = !state
if !city then set policy new_policy [operator][city] = !city

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_policy = true
goto check-policy

:config-policy:
on error goto config-policy-error
config from policy where id=!operator_id

:end-script:
end script

:terminate-scripts:
exit scripts

:ip-error:
print "An Operator node policy with the same company and node name already exists under a different IP address: " !ip_address
goto terminate scripts

:sign-policy-error:
print "Failed to sign operator policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member operator policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare operator policy on blockchain"
goto terminate-scripts

#----------------------------------------------------------------------------------------------------------------------#
# Create policy for query, query or publisher
#   --> check if policy exists
#   --> prepare policy
#   --> declare policy
#   --> recheck
# :sample-policy:
#   {"query": {
#       "name": "anylog-query",
#       "company": "AnyLog Co.",
#       "ip": "136.23.47.189",
#       "internal_ip": "136.23.47.189",
#       "port": 32348,
#       "rest_port": 32349,
#       "loc": "37.425423, -122.078360",
#       "country": "US",
#       "state": "CA",
#       "city": "Mountain View"
#   }}
#----------------------------------------------------------------------------------------------------------------------#

:check-policy:
is_policy = blockchain get query where company=!company_name and name=!node_name
if !is_policy then goto end-script
if not !is_policy and !create_policy == true then goto declare-policy-error

:create-policy:
set new_policy = ""
set policy new_policy [query] = {}
set policy new_policy [query][name] = !node_name
set policy new_policy [query][company] = !company_name

:network-querys:
if !overlay_ip and !tcp_bind == true then set policy new_policy [query][ip] = !overlay_ip
if not !overlay_ip and !tcp_bind == true then set policy new_policy [query][ip] = !ip
if !overlay_ip and !tcp_bind == false then
do set policy new_policy [query][ip] = !external_ip
do set policy new_policy [query][internal_ip] = !overlay_ip
if not !overlay_ip and !tcp_bind == false then
do set policy new_policy [query][ip] = !external_ip
do set policy new_policy [query][internal_ip] = !ip

set policy new_policy [query][port] = !anylog_server_port.int
set policy new_policy [query][rest_port] = !anylog_rest_port.int
if !anylog_broker_port then set policy new_policy [query][rest_port] = !anylog_broker_port.int

if !license_key then set policy new_policy [query][license] = !license_key

:location:
if !loc then set policy new_policy [query][loc] = !loc
if !country then set policy new_policy [query][country] = !country
if !state then set policy new_policy [query][state] = !state
if !city then set policy new_policy [query][city] = !city

:publish-policy:
process !local_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error
set create_policy = true
goto check-policy

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign query policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member query policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare query policy on blockchain"
goto terminate-scripts

#----------------------------------------------------------------------------------------------------------------------#
# Create policy for publisher
#   --> check if policy exists
#   --> prepare policy
#   --> declare policy
#   --> recheck
# :sample-policy:
#   {"publisher": {
#       "name": "anylog-publisher",
#       "company": "AnyLog Co.",
#       "ip": "136.23.47.189",
#       "local_ip": "136.23.47.189",
#       "port": 32248,
#       "rest_port": 32249,
#       "loc": "37.425423, -122.078360",
#       "country": "US",
#       "state": "CA",
#       "city": "Mountain View"
#   }}
#----------------------------------------------------------------------------------------------------------------------#
on error ignore
set create_policy = false

:check-policy:
process !local_scripts/policies/validate_policy.al

# just created the policy + exists
if !is_policy and !create_policy == true then goto end-script

# policy pre-exists - validate IP addresses
if !is_policy and not !create_policy == false  then
do ip_address = from !is_policy bring [*][ip]
do if !ip_address != !external_ip and !ip_address != !ip and !ip_address != !overlay_ip then goto ip-error
do goto end-script

# failure show created policy
if not !is_policy and !create_policy == true then goto declare-policy-error

:create-policy:
set new_policy = ""
set policy new_policy [publisher] = {}
set policy new_policy [publisher][name] = !node_name
set policy new_policy [publisher][company] = !company_name

:network-publisher:
if !tcp_bind == false then
do set policy new_policy [publisher][ip] = !external_ip
do if !overlay_ip then set policy new_policy [publisher][local_ip] = !overlay_ip
do if not !overlay_ip and !proxy_ip then set policy new_policy [publisher][local_ip] = !proxy_ip
do if not !overlay_ip and not !proxy_ip then set policy new_policy [publisher][local_ip] = !ip

if !tcp_bind == true then
do if !overlay_ip then set policy new_policy [publisher][ip] = !overlay_ip
do if not !overlay_ip and !proxy_ip then set policy new_policy [publisher][ip] = !proxy_ip
do if not !overlay_ip and not !proxy_ip then set policy new_policy [publisher][ip] = !ip

if !rest_bind == true then
do if !overlay_ip then set policy new_policy [publisher][rest_ip] = !overlay_ip
do if not !overlay_ip and !proxy_ip then set policy new_policy [publisher][rest_ip] = !proxy_ip
do if not !overlay_ip and not !proxy_ip then set policy new_policy [publisher][rest_ip] = !ip

if !broker_bind == true then
do if !overlay_ip then set policy new_policy [publisher][broker_ip] = !overlay_ip
do if not !overlay_ip and !proxy_ip then set policy new_policy [publisher][broker_ip] = !proxy_ip
do if not !overlay_ip and not !proxy_ip then set policy new_policy [publisher][broker_ip] = !ip


if !overlay_ip and !proxy_ip then set policy new_policy[publisher][proxy] = !proxy_ip

set policy new_policy [publisher][port] = !anylog_server_port.int
set policy new_policy [publisher][rest_port] = !anylog_rest_port.int
if !anylog_broker_port then set policy new_policy [publisher][broker_port] = !anylog_broker_port.int

:location:
if !loc then set policy new_policy [publisher][loc] = !loc
if !country then set policy new_policy [publisher][country] = !country
if !state then set policy new_policy [publisher][state] = !state
if !city then set policy new_policy [publisher][city] = !city

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_policy = true
goto check-policy

:end-script:
end script

:terminate-scripts:
exit scripts

:ip-error:
print "A Publisher node policy with the same company and node name already exists under a different IP address: " !ip_address
goto terminate scripts


:sign-policy-error:
print "Failed to sign publisher policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member publisher policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare publisher policy on blockchain"
goto terminate-scripts

#--------------------------------------------------------------------------------------------------#
# Declare node policy for EdgeX
#   - set params
#   - check if policy (id) exists
#   - create policy (if DNE) + recheck
#   - declare policy
#:sample-policy:
# {'edgex': {
#        'ip': '172.105.4.104',
#        'local_ip': '172.105.4.104',
#        'name': 'edgex-insight',
#        'company': 'New Company',
#        'hostname': 'anylog-master',
#        'loc': '43.6496,-79.3833',
#        'country': 'CA',
#        'state': 'Ontario',
#        'city': 'Toronto',
#        'url': '172.105.4.104:9090',
#        'id': '08c2ac547b4462e3d761d5d6597a77f8',
#        'date': '2023-07-16T01:10:35.569033Z'
# }}
#--------------------------------------------------------------------------------------------------#
# process !local_scripts/deployment_scripts/policies/edgex_node_policy.al

:set-params:
policy_type = edgex
policy_name = edgex-insight
schedule_time = 15 seconds
if not !monitor_node_company then monitor_node_company = !company_name
if not !monitor_node then set monitor_node = query
check_count = 0
edgex_url = "http://" + !external_ip + ":9090"

:check-policy:
on error goto prepare-policy

<policy_id = blockchain get !policy_type where
    name = !policy_name and
    hostname = !hostname
    company = !company_name and
    ip = !external_ip and
    local_ip = !ip
bring [!policy_type][id]>

if !is_policy then goto end-script

:prepare-policy:
on error ignore
set policy new_policy [!policy_type] = {}
set policy new_policy [!policy_type][ip]= !external_ip
set policy new_policy [!policy_type][local_ip]= !ip

if !node_name then set policy new_policy [!policy_type][name] = !policy_name
if !company_name then set policy new_policy [!policy_type][company] = !company_name
if !hostname then set policy new_policy [!policy_type][hostname] = !hostname
if !loc then set policy new_policy [!policy_type][loc] = !loc
if !country then set policy new_policy [!policy_type][country] = !country
if !state then set policy new_policy [!policy_type][state] = !state
if !city then set policy new_policy [!policy_type][city] = !city

# GUI access for EdgeX
set policy new_policy [!policy_type][url] = !url

:declare-policy:
on error goto declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
check_count = 1
goto check-policy

:declare-policy:
on error goto declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn


:end-script:
end script


:check-policy-error:
echo "Failed to check of EdgeX policy exists"
goto prepare-policy

:failed-to-declare-policy:
echo "Failed to declare EdgeX policy, cannot continue..."
goto end-script

:declare-policy-error:
echo "Failed to declare policy for EdgeX node"
goto end-script

:run-policy-error:
echo "Failed to execute script associated with EdgeX policy"
goto end-script


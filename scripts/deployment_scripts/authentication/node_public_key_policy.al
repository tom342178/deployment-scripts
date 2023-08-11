#------------------------------------------------------------------------------------------------------------
# Create member policy for node
#------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/node_public_key_policy.al

:declare-policy:
on error ignore
set policy new_policy [member] = {}
set policy new_policy [member][name] = !node_name
set policy new_policy [member][type] = "node"

if !tcp_bind == false then
do set policy new_policy [member][ip] = !external_ip
do set policy new_policy [member][local_ip] = !ip
do if !overlay_ip then set policy new_policy [member][local_ip] = !overlay_ip

if !tcp_bind == true then
do set policy new_policy [member][ip] = !ip
do if !overlay_ip then set policy new_policy [member][ip] = !overlay_ip

set policy new_policy [member][key] = !public_key

:validate-policy:
on error goto validate-policy-error
test_policy = json !new_policy
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:validate-policy-error:
echo "Error: Issue with cluster policy declaration"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for " !policy_type
return
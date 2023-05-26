#-----------------------------------------------------------------------------------------------------------------------
# Script to deploy a policy of type: Master, Query or Publisher node
#
#   ** The information provided for the blockchain policy will be used to connect the node to the network **
#
# ---- Sample Policy ---
# {'publisher' : {
#       'hostname' : 'al-live-publisher',
#       'name' : 'anylog-publisher-node',
#       'ip' : '172.104.180.110',
#       'local_ip' : '172.104.180.110',
#       'company' : 'AnyLog',
#       'port' : 32248,
#       'rest_port' : 32249,
#       'loc' : '1.2897,103.8501',
#       'country' : 'SG',
#       'state' : 'Singapore',
#       'city' : 'Singapore',
#       'id' : 'd2ef8f32b3d894f4d721275435e7d05d',
#       'date' : '2022-06-06T00:38:45.838582Z',
#       'ledger' : 'global'
# }}
# ---- Sample Policy ---
#
# -- Notes --
#   1. When binding is set to True, AnyLog will bind against the local or overlay IP address for TCP. However, by default
#      AnyLog does not bind on either REST or Message Broker because data and/or GET requests against those port
#      could come from machines that are not part of the network.
#   2. Users can extend their policy to include a distinction between internal ports and external ports by adding
#      `local_` prior to the component. Example
#         {'publisher' : {
#               ...
#               'ip' : '172.194.183.124',
#               'local_ip' : '192.168.0.174',
#               'company' : 'AnyLog',
#               'port' : 32248,
#               'local_port': 2248,
#               'rest_port' : 32249,
#               'local_rest_port': 2249
#               ...
#         }}
#   3. If the `proxy_ip` is declared, it will not used, but rather more of an FYI regarding network configuration
#      of the actual machine.
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/declare_config_policy.al



:check-policy:
on error ignore
is_policy = blockchain get config where name = !config_policy_name and company = !company_name
if !is_policy then
do echo "Notice: Config Policy " + !config_policy_name + " already exists"
do goto end-script

:prep-policy:
on error ignore
process !local_scripts/deployment_scripts/policies/prepare_config_policy.al

:sign-policy:
if !enable_auth == true then
do on error goto sign-policy-error
do id sign !new_policy where key = !private_key and password = !node_password

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

:sign-policy-error:
echo "Error: Failed to sign cluster policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with cluster policy declaration"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for " !policy_type
return
Footer

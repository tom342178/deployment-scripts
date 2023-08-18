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
# process !local_scripts/deployment_scripts/policies/declare_node_policy.al

:check-policy:
on error ignore
process !local_scripts/deployment_scripts/policies/validate_node_policy.al
if !is_policy thengoto end-script

:prep-policy:
on error ignore
process !local_scripts/deployment_scripts/policies/prepare_node_policy.al

:publish-policy:
process !local_scripts/deployment_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:sign-policy-error:
echo "Failed to sign " + !node_type + " policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare member " + !node_type " policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to declare " + !node_type " policy on blockchain"
goto terminate-scripts

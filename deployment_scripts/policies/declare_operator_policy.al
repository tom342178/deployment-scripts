#-----------------------------------------------------------------------------------------------------------------------
# Script to deploy a policy of type: Operator node
#
# ---- Sample Policy ---
# {'operator' : {
#       'hostname' : 'al-live-operator1',
#       'name' : 'anylog-cluster1-operator1',
#       'ip' : '139.162.126.241',
#       'local_ip' : '139.162.126.241',
#       'company' : 'Lit San Leandro',
#       'port' : 32148,
#       'rest_port' : 32149,
#       'cluster' : '0015392622f3eaac70eafa4311fc2338',
#       'member' : 12,
#       'loc' : '35.6895,139.6917',
#       'country' : 'JP',
#       'state' : 'Tokyo',
#       'city' : 'Tokyo',
#       'id' : '034c7bb7cea08f7571ef99d9a0ce37c9',
#       'date' : '2022-06-04T22:48:00.498640Z',
#       'ledger' : 'global'
# }}
# ---- Sample Policy ---
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/declare_operator_policy.al

:check-policy:
on error ignore
process !local_scripts/deployment_scripts/policies/validate_node_policy.al
if !is_policy then
do echo "Notice: " + !policy_type + " policy " + !node_name + " already exists"
do goto end-script

:get-cluster:
if not !cluster_id then cluster_id = blockchain get cluster where name=!cluster_name and company=!company_name bring.first [cluster][id]
if not !cluster_id then goto missing-cluster-error

:prep-policy:
on error ignore
process !local_scripts/deployment_scripts/policies/prepare_node_policy.al

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

:missing-cluster-error:
echo "Error: Unable to declare operator policy - process will complete but node will not offically be part of the network"
goto end-scripts

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

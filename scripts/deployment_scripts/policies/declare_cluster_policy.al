#-----------------------------------------------------------------------------------------------------------------------
# Script to deploy a policy of type cluster
#
# ---- Sample Policy ---
# {'cluster' : {
#       'company' : 'Lit San Leandro',
#       'dbms' : 'litsanleandro',
#       'name' : 'litsanleandro-cluster1',
#       'id' : '0015392622f3eaac70eafa4311fc2338',
#       'date' : '2022-06-04T22:47:48.479532Z',
#       'status' : 'active',
#       'ledger' : 'global'
# }}
# ---- Sample Policy ---
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/declare_cluster_policy.al

:check-policy:
on error ignore
is_policy = blockchain get cluster where name=!cluster_name and company=!company_name bring.first
if !is_policy then
do echo "Notice: Cluster Policy " + !cluster_name + " already exists"
do goto end-script

:prep-policy:
on error ignore
if !default_dbms then
<do new_policy = {"cluster": {
    "company": !company_name,
    "name": !cluster_name,
    "dbms": !default_dbms
}}>
<else new_policy = {"cluster": {
    "company": !company_name,
    "name": !cluster_name
}}>

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

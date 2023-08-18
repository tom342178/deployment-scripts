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
if !is_policy then goto end-script

:prep-policy:
on error ignore
<new_policy = {"cluster": {
    "company": !company_name,
    "name": !cluster_name
}}>

#if !default_dbms then
#<do new_policy = {"cluster": {
#    "company": !company_name,
#    "name": !cluster_name,
#    "dbms": !default_dbms
#}}>
#<else new_policy = {"cluster": {
#    "company": !company_name,
#    "name": !cluster_name
#}}>

:publish-policy:
process !local_scripts/deployment_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:sign-policy-error:
echo "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to declare cluster policy on blockchain"
goto terminate-scripts
#----------------------------------------------------------------------------------------------------------------------
# Process:
#   1. declare policy (if DNE)
#   2. extract policy_id
#----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/declare_policies.al

:declare-policy:
if !policy_based_networking == true then
do process !local_scripts/deployment_scripts/policies/declare_config_policy.al
do call reset-new-policy 

if $NODE_TYPE == rest then goto get-id

if !deploy_ledger == true then
do policy_type  = master
do process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do call reset-new-policy 

if $NODE_TYPE == ledger or $NODE_TYPE == master then goto get-id

if !deploy_operator == true then
do process !local_scripts/deployment_scripts/policies/declare_cluster_policy.al
do call reset-new-policy 
do set policy_type = operator
do cluster_id = blockchain get cluster where name=!cluster_name and company=!company_name bring.first [*][id]
do process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do call reset-new-policy 

if $NODE_TYPE == operator or $NODE_TYPE == standalone then goto get-id

if !deploy_publisher == true then
do set policy_type = publisher
do process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do call reset-new-policy 

if $NODE_TYPE == publisher or $NODE_TYPE == standalone-publisher then goto get-id

if !deploy_query == true then
do set policy_type = query
do process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do call reset-new-policy 

:get-id:
if !policy_based_networking == true then
do policy = blockchain get config where name = !config_policy_name and company = !company_name
do if !policy then goto get-policy-id

if !deploy_ledger == true then
do policy_type  = master
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do goto get-policy-id

if !deploy_operator == true then
do set policy_type = operator
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do goto get-policy-id

if !deploy_publisher == true then
do set policy_type = publisher
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do goto get-policy-id

if !deploy_query == true then
do set policy_type = query
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do goto get-policy-id

:get-policy-id:
on error call get-id-error
if !policy then policy_id = from !policy bring.first [*][id]
else goto get-id-error 

:end-script:
end script

:reset-new-policy: 
set new_policy = "" 
return 


:get-id-error:
echo "Error: Failed  to get policy ID."
goto end-script



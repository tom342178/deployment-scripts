#----------------------------------------------------------------------------------------------------------------------
# Process:
#   1. declare policy (if DNE)
#   2. extract policy_id
#----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/declare_policies.al

call reset-new-policy

:declare-policy:
if !deploy_ledger == true then
do policy_type  = master
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then call check-policy-error
do call reset-new-policy 

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
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then call check-policy-error
do call reset-new-policy

if !deploy_query == true then
do set policy_type = query
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then process !local_scripts/deployment_scripts/policies/declare_node_policy.al
do process !local_scripts/deployment_scripts/policies/validate_node_policy.al
do if not !is_policy then call check-policy-error
do call reset-new-policy 

:end-script:
end script

:reset-new-policy: 
set new_policy = "" 
return 


:check-policy-error:
echo "Error: Failed to declare policy of type " !policy_type
goto end-script



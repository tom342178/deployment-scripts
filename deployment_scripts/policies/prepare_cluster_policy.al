#---------------------------------------------------------------------------------------------------------------
# code for checking whether a cluster policy exists. If not, then prepare one to be declared
#---------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/policies/prepare_cluster_policy.al

:prepare-policy:
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

:end-script:
end script
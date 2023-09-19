#-----------------------------------------------------------------------------------------------------------------------
# partition data & set scheduler of how often the data is removed
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/data_partitioning.al

on error ignore

process !local_scripts/deployment_scripts/policies/validate_node_policy.al
if !is_policy then is_scripts = from !is_policy bring [*][script]
if not !is_policy or not !is_scripts then goto set-partition
policy_id = from !is_policy bring [*][id]

on error goto set-partition
config from policy where id = !policy_id
goto end-script

:set-partition:
on error call set-partition-error
if !enable_partitions == false then goto end-script 

partition !default_dbms !table_name using !partition_column by !partition_interval

on error call set-partition-scheduler-error
schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep

:end-script:
end script

:set-partition-error:
echo "Error: Failed to set partitions"
return

:set-partition-scheduler-error:
echo "Error: Failed to set clean partitioning scheduled process"
return


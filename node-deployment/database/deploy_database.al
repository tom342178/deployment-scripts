#----------------------------------------------------------------------------------------------------------------
# Deploy database(s) based on node type and configuration
# -- for operator also deploy partitions if set
#----------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/deploy_database.al


on error ignore

# Code configures blockchain database + ledger table if node_type == master and also blockchain sync (for all)
process !local_scripts/database/configure_dbms_blockchain.al

if !node_type == operator then process !local_scripts/database/configure_dbms_operator.al
if !node_type == operator or !enable_nosql == true then process !local_scripts/database/configure_dbms_nosql.al
if !node_type == operator and !enable_partitions == true then
do partition !default_dbms !table_name using !partition_column by !partition_interval
do schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep

if !node_type == operator or !node_type == publisher then process !local_scripts/database/configure_dbms_almgm.al
if !deploy_system_query == true then process !local_scripts/database/configure_dbms_system_query.al

:end-script:
end script
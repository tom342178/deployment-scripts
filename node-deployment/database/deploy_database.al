#----------------------------------------------------------------------------------------------------------------
# Deploy database(s) based on node type and configuration
# -- for operator also deploy partitions if set
#----------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/deploy_database.al

on error ignore

if !debug_mode.int > 0 then set debug on

# Code configures blockchain database + ledger table if node_type == master and also blockchain sync (for all)
if !debug_mode.int == 2 then
do set debug interactive
do print "Blockchain related database processes"
do set debug on
do thread !local_scripts/database/configure_dbms_blockchain.al
else process !local_scripts/database/configure_dbms_blockchain.al

if (!node_type == operator or $NODE_TYPE == master-operator) and !enable_partitions == true and !debug_mode.int == 2 then
do set debug interactive
do print "Deploy operator databases"
do set debug on
do thread !local_scripts/database/configure_dbms_operator.al
do thread !local_scripts/database/configure_dbms_nosql.al
else if !node_type == operator or $NODE_TYPE == master-operator then
do process !local_scripts/database/configure_dbms_operator.al
do process !local_scripts/database/configure_dbms_nosql.al

if (!node_type == operator or $NODE_TYPE == master-operator) and !enable_partitions == true and !debug_mode.int == 2 then
do set debug interactive
do print "Set partitions"

if (!node_type == operator or $NODE_TYPE == master-operator) and !enable_partitions == true then
do partition !default_dbms !table_name using !partition_column by !partition_interval
do schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep

 if !debug_mode.int == 2 then set debug on

if (!node_type == operator or $NODE_TYPE == master-operator) and !debug_mode.int == 2 then
do set debug interactive
do print "Deploy almgm database"
do set debug on
do thread !local_scripts/database/configure_dbms_almgm.al
else if !node_type == operator or !node_type == publisher or $NODE_TYPE == master-operator or $NODE_TYPE == master-publisher  then process !local_scripts/database/configure_dbms_almgm.al

if (!node_type == operator or $NODE_TYPE == master-operator) and !enable_partitions == true and !deploy_system_query == true and !debug_mode.int == 2 then
do set debug interactive
do print "Deploy system_query database"
do set debug on
do thread !local_scripts/database/configure_dbms_system_query.al
else if !deploy_system_query == true then process !local_scripts/database/configure_dbms_system_query.al

:end-script:
end script
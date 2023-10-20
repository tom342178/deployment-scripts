#----------------------------------------------------------------------------------------------------------------
# Deploy database(s) based on node type and configuration
#----------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/deploy_database.al

set debug off
on error ignore

if !node_type == master then process !local_scripts/database/configure_dbms_blockchain.al
if !node_type == operator then process !local_scripts/database/configure_dbms_operator.al
if !node_type == operator or !enable_nosql == true then process !local_scripts/database/configure_dbms_nosql.al
if !node_type == operator or !node_type == publisher then process !local_scripts/database/configure_dbms_almgm.al
if !deploy_system_query == true then process !local_scripts/database/configure_dbms_system_query.al

:end-script:
end script
#----------------------------------------------------------------------------------------------------------------
# Deploy database(s) based on node type and configuration
# -- for operator also deploy partitions if set
#----------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/deploy_database.al
set debug on
on error ignore
if !debug_mode == true then set debug on

if $NODE_TYPE == operator then goto operator-dbms
if $NODE_TYPE == publisher then goto almgm-dbms
if $NODE_TYPE == query then goto system-query-dbms

:master-dbms:
if !debug_mode == true then print "Blockchain related database processes"
process !local_scripts/database/configure_dbms_blockchain.al
if $NODE_TYPE == master-publisher then goto almgm-dbms
else goto system-query-dbms

:operator-dbms:
if !debug_mode == true then print "Operator related database processes"
process !local_scripts/database/configure_dbms_operator.al
process !local_scripts/database/configure_dbms_nosql.al

:almgm-dbms:
if !debug_mode == true then print "almgm related database processes"
process !local_scripts/database/configure_dbms_almgm.al

:system-query-dbms:
if !node_type != query and !system_query != true then goto blockchain-sync
if !debug_mode == true then print "system_query database processes"
else process !local_scripts/database/configure_dbms_system_query.al


:blockchain-sync:
if !debug_mode == true then print "set blockchain sync"

on error call blockchain-sync-error

<if !blockchain_source == master then run blockchain sync where
    source=master and
    time=!blockchain_sync and
    dest=!blockchain_destination and
    connection=!ledger_conn>
<else run blockchain sync where
    source = blockchain and
    time = !blockchain_sync and
    dest=!blockchain_destination and
    platform = optimism>

set debug off
:end-script:
end script

:terminate-scripts:
exit scripts

:blockchain-sync-error:
echo "failed to to declare blockchain sync process"
goto terminate-scripts



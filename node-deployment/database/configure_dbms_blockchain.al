#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for master node
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/configure_dbms_blockchain.al

on error ignore
if !node_type != master and $NODE_TYPE != master-operator and $NODE_TYPE != master-publisher then goto blockchain-sync

:ledger-dbms:
on error goto ledger-db-error
<if !db_type == psql then connect dbms blockchain where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port and
    autocommit = !autocommit and
    unlog = !unlog>
else if !db_type == sqlite then connect dbms blockchain where type=!db_type

on error goto ledger-table-error
is_table = info table blockchain ledger exists
if !is_table == false then create table ledger where dbms=blockchain

:blockchain-sync:
on error call blockchain-sync-error
<run blockchain sync where
    source=!blockchain_source and
    time=!blockchain_sync and
    dest=!blockchain_destination and
    connection=!ledger_conn
>

:end-script:
end script

:terminate-scripts:
exit scripts

:ledger-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto terminate-scripts

:ledger-table-error:
echo "Error: Failed to create table blockchain.ledger. Cannot continue"
goto terminate-scripts

:blockchain-sync-error:
echo "failed to to declare blockchain sync process"
goto terminate-scripts



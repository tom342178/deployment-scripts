#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for master node
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/configure_dbms_blockchain.al

:ledger-dbms:
on error goto ledger-db-error
<if !db_type == psql then connect dbms blockchain where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port>
else if !db_type == sqlite then connect dbms blockchain where type=!db_type

on error goto ledger-table-error
is_table = info table blockchain ledger exists
if !is_table == false then create table ledger where dbms=blockchain

:end-script:
end script

:terminate-scripts:
exit scripts

:ledger-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto terminate-scripts

#if !db_type != sqlite then
#do echo "Error: Failed to declare blockchain database with database type " !db_type " will reattempt with SQLite"
#do set db_type = sqlite
#do goto ledger-dbms
#else !db_type == sqlite
#do echo "Error: Unable to connect to blockchain database with db type: SQLite. Cannot return"
#do goto terminate-scripts

:ledger-table-error:
echo "Error: Failed to create table blockchain.ledger. Cannot continue"
goto terminate-scripts




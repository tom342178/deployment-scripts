#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for operator node
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/configure_dbms_operator.al

:operator-dbms:
on error goto operator-db-error
if !db_type == psql then
<do connect dbms !default_dbms where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port.int and
    autocommit = !autocommit
>
else connect dbms !default_dbms where type=!db_type

:end-script:
end script

:terminate-scripts:
exit scripts

:operator-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto terminate-scripts

#if !db_type != sqlite then
#do echo "Error: Failed to declare " !default_dbms" database with database type " !db_type " will reattempt with SQLite"
#do set db_type = sqlite
#do goto operator-dbms
#else !db_type == sqlite
#do echo "Error: Unable to connect to " !default_dbms " database with db type: SQLite. Cannot continue"
#do goto terminate-scripts

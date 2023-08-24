#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for system_query
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/configure_dbms_system_query.al
:system-query-dbms:
on error goto system-query-db-error
if !db_type == sqlite or !memory == true then connect dbms system_query where type=sqlite and memory=!memory
<else connect dbms system_query where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port.int>

:end-script:
end script


:system-query-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto end-script

#if !db_type != sqlite then
#do echo "Error: Failed to declare system_query database with database type " !db_type " will reattempt with SQLite"
#do set db_type = sqlite
#do goto operator-dbms
#else !db_type == sqlite
#do echo "Error: Unable to connect to database with db type: SQLite"
#do goto end-script

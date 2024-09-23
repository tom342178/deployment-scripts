#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for system_query
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/configure_dbms_system_query.al

if !debug_mode.int > 0 then set debug on
if !debug_mode.int == 2 then
do set debug interactive
do print "deploy system_query logical databasae"
do set debug on

:system-query-dbms:
on error goto system-query-db-error
if !db_type == sqlite and !memory == true then connect dbms system_query where type=sqlite and memory=!memory
if !db_type == sqlite and !memory == false then connect dbms system_query where type=sqlite
<if !db_type == psql then connect dbms system_query where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port and
    autocommit = !autocommit and
    unlog = !memory>

:end-script:
end script


:system-query-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto end-script
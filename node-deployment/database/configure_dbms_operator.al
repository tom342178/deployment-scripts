#-----------------------------------------------------------------------------------------------------------------------
# Based on node_type create relevant databases / tables for operator node
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/database/configure_dbms_operator.al

if !debug_mode.int > 0 then set debug on

if !debug_mode.int == 2 then
do set debug interactive
do print "Deploy local database !default_dbms"
do set debug on

:operator-dbms:
on error goto operator-db-error
if !db_type == psql then
<do connect dbms !default_dbms where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port and
    autocommit = !autocommit and
    unlog = !unlog
>
else connect dbms !default_dbms where type=!db_type

:end-script:
end script

:terminate-scripts:
exit scripts

:operator-db-error:
echo "Error: Unable to connect to almgm database with db type: " !db_type ". Cannot continue"
goto terminate-scripts


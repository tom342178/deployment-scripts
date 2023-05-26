#-----------------------------------------------------------------------------------------------------------------------
# Process to restart `system_query` database
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_system_query.al

set error = false
:disconnect:
on error call disconnect-error
disconnect dbms system_query

:psql:
on error call drop-error
if !db_type == psql then drop dbms system_query from psql where user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

:sqlite:
on error call drop-error
if !db_type == sqlite then drop dbms system_query from sqlite


:reconnect:
on error ignore
# if error is true there's no need to restart database
if error == false then process !local_scripts/deployment_scripts/configure_dbms_system_query.al

:end-script:
end script

:disconnect-error:
echo "Error: Failed to disconnect from `system_query` logical database"
goto end-script

:psql-error:
echo "Error: Failed to drop `system_query` logical database"
set error = true
return
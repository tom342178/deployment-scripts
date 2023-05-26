#-----------------------------------------------------------------------------------------------------------------------
# Process to restart `!default_dbms` (SQL) database
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_default_dbms.al

set error = false
:disconnect:
on error call disconnect-error
disconnect dbms !default_dbms

:psql:
on error call drop-error
if !db_type == psql then drop dbms !default_dbms from psql where user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

:sqlite:
on error call drop-error
if !db_type == sqlite then drop dbms !default_dbms from sqlite


:reconnect:
on error ignore
# if error is true there's no need to restart database
if error == false then process !local_scripts/deployment_scripts/configure_dbms_operator.al

:end-script:
end script

:disconnect-error:
echo "Error: Failed to disconnect from `!default_dbms` logical database"
goto end-script

:psql-error:
echo "Error: Failed to drop `!default_dbms` logical database"
set error = true
return
#-----------------------------------------------------------------------------------------------------------------------
# Process to restart `almgm` database and `tsd_info` table(s) 
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_almgm.al

set error = false
:disconnect:
on error call disconnect-error
disconnect dbms almgm

:psql:
on error call drop-error
if !db_type == psql then drop dbms almgm from psql where user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

:sqlite:
on error call drop-error
if !db_type == sqlite then drop dbms almgm from sqlite


:reconnect:
on error ignore
# if error is true there's no need to restart database
if error == false then process !local_scripts/deployment_scripts/configure_dbms_almgm.al

:end-script:
end script

:disconnect-error:
echo "Error: Failed to disconnect from `almgm` logical database"
goto end-script

:psql-error:
echo "Error: Failed to drop `almgm` logical database"
set error = true
return
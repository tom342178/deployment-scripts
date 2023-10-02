#-----------------------------------------------------------------------------------------------------------------------
# Process to restart `!default_dbms` (NoSQL) database
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_default_dbms_nosql.al

set error = false

:get-blobs-db:
on error goto blobs-db-error
cluster_id = blockchain get operator bring [*][cluster]
blobs_dbms = blockchain get cluster where id = !cluster_id  bring [*][dbms]  "_blobs"

:disconnect:
on error call disconnect-error
disconnect dbms !blobs_dbms

:drop-dbms:
on error call drop-error
drop dbms !default_dbms from !nosql_type where user = !nosql_user and password = !nosql_passwd and ip = !nosql_ip and port = !nosql_port


:reconnect:
on error ignore
# if error is true there's no need to restart database
if error == false then process !local_scripts/deployment_scripts/configure_dbms_nosql.al

:end-script:
end script

:disconnect-error:
echo "Error: Failed to disconnect from `!default_dbms` logical database"
goto end-script

:psql-error:
echo "Error: Failed to drop `!default_dbms` logical database"
set error = true
return
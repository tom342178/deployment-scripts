#-----------------------------------------------------------------------------------------------------------------------
# Rest Operator Node
#   --> exit operator
#   --> delete blockchain file
#   --> reset databases
#       --> call process that reset almgm database
#       --> reset default dbms
# <---------            Restarting Operator Node        --------->
# Steps to restart operator node:
#   1) Declare Cluster policy: process !local_scripts/deployment_scripts/declare_cluster.al
#   2) Declare Operator policy: process !local_scripts/deployment_scripts/declare_operator.al
#   3) Execute `run operator`: process !local_scripts/deployment_scripts/deploy_operator.al
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_operator.al

:exit-operator:
on error call exit-operator-error
exit operator

:drop-files:
on error call drop-files-error
time file drop all

:remove-local-blockchain:
on error call remove-local-blockchain-error
blockchain delete local file

:reconnect-dbms:
on error ignore
process !local_scripts/deployment_scripts/configure_dbms_operator.al
process !local_scripts/reset_node/reset_almgm.al

:reset-default-dbms:
on error goto disconnect-default-error
if !default_dbms then disconnect dbms !default_dbms

if !db_type == psql then
do on error goto postgres-connect-error
do connect dbms postgres where type=!db_type and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port
do on error ignore
do drop dbms !default_dbms where type=!db_type and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port
do on error call postgres-disconnect-error
do disconnect dbms postgres
else if !db_type == sqlite then
do on error call drop-table-error
do drop dbms !default_dbms where type=!db_type

:end-script:
end script

:exit-operator-error:
echo "Error: Failed to stop operator process"
return

:drop-files-error:
echo "Error: Failed to drop files"
return

:remove-local-blockchain-error:
echo "Error: Failed to drop local file copy of blockchain"
return

:disconnect-default-error:
echo "Error: Failed to disconnect from default database " !default_dbms ". Cannot reset default database"
goto end-script

:postgres-connect-error:
echo "Error: Failed to connect to postgres logical database. Cannot reset default database"
goto end-script

:drop-table-error:
echo "Error: Failed to drop " !default_dbms " logical database."
return

:postgres-disconnect-error:
echo "Error: Failed to disconnect from postgres logical database"
return

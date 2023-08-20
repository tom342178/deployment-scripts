#-----------------------------------------------------------------------------------------------------------------#
# For master node:
#   --> declare blockchain logical database and table
#   --> deploy system_query logical database if param is set
#   --> run schedular and blockchain sync
#   --> declare blockchain policy
#-----------------------------------------------------------------------------------------------------------------#
# process !local_scripts/run_scripts/start_master.al

on error ignore
:run-processes:
process !local_scripts/deployment_scripts/database/configure_dbms_blockchain.al
if !deploy_system_query == true then process !local_scripts/deployment_scripts/database/configure_dbms_system_query.al

:end-script:
end script

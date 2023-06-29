#-----------------------------------------------------------------------------------------------------------------#
# For operator node:
#   --> declare operator relatedd database and almgm logical database and table
#   --> deploy system_query logical database if param is set
#   --> run schedular and blockchain sync
#   --> declare blockchain policy
#   --> start `run operator` process (3-steps)
#-----------------------------------------------------------------------------------------------------------------#
# process !local_scripts/run_scripts/start_operator.al

on error ignore
:run-processes:
process !local_scripts/deployment_scripts/database/configure_dbms_operator.al
if !enable_nosql == true then process !local_scripts/deployment_scripts/database/configure_dbms_nosql.al
process !local_scripts/deployment_scripts/database/configure_dbms_almgm.al
if !deploy_system_query == true then process !local_scripts/deployment_scripts/database/configure_dbms_system_query.al

process !local_scripts/deployment_scripts/run_scheduler.al

process !local_scripts/deployment_scripts/data_partitioning.al
process !local_scripts/deployment_scripts/pre_deployment.al
process !local_scripts/deployment_scripts/deploy_operator.al


:end-script:
end script

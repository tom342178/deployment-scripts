#-----------------------------------------------------------------------------------------------------------------#
# For query node:
#   --> deploy system_query logical database
#   --> run schedular and blockchain sync
#-----------------------------------------------------------------------------------------------------------------#
# process !local_scripts/run_scripts/start_query.al

on error ignore
:run-processes:
process !local_scripts/deployment_scripts/database/configure_dbms_system_query.al

process !local_scripts/deployment_scripts/run_scheduler.al

:end-script:
end script

#-----------------------------------------------------------------------------------------------------------------------
# Run scheduling processes
# --> run schedule 1
# --> run blockchain sync
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/run_scheduler.al

:blockchain-sync:
if $NODE_TYPE != rest and $NODE_TYPE != none  and $NODE_TYPE != edgex then
do on error call blockchain-sync-error
do run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn

:set-scheduler:
on error goto scheduler-error1
run scheduler 1

:end-script:
end script

:terminate-scripts:
exit scripts

:call scheduler-error1:
echo "Error: Failed to set Scheduler 1. Cannot continue"
goto terminate-scripts

:blockchain-sync-error:
echo "Error: Failed to set blockchain sync"
goto end-script


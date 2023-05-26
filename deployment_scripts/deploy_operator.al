#-----------------------------------------------------------------------------------------------------------------------
# Deployment code specifically for operator node
# --> data distribution
# --> blockchain get
# --> run operator
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/deploy_operator.al

:enable-ha:
if !enable_ha == true then
do on error call data-distributor-error
do run data distributor
do on error call data-consumer-error
do run data consumer where start_date = !ha_start_date

:blockchain-get:
on error ignore
operator_id = blockchain get operator where name = !node_name and company=!company_name bring [*][id] 
if not !operator_id then goto blockchain-get-error

:run-operator:
on error goto operator-error
<run operator where
    create_table=!create_table and
    update_tsd_info=!update_tsd_info and
    compress_json=!compress_file and
    compress_sql = !compress_file and archive=!archive and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads = !operator_threads
>

:end-script:
end script

:terminate-scripts:
exit scripts

:data-distributor-error:
echo "Error: Failed to run data distributor"
return

:data-consumer-error:
echo "Error: Failed to run data consumer"
return

:blockchain-get-error:
echo "Failed to get Operator ID from blockchain. Cannot execute `run operator` code`"
goto terminate-scripts

:operator-error:
echo "Error: Failed to start operator process"
goto terminate-scripts



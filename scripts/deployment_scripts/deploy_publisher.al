#-----------------------------------------------------------------------------------------------------------------------
# Deployment code specifically for publisher node
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/deploy_publisher.al

:run-publisher:
on error goto publisher-error
<run publisher where
    compress_json=!publisher_compress_file and 
    compress_sql=!publisher_compress_file and
    master_node=!ledger_conn and
    dbms_name=!dbms_file_location and
    table_name=!table_file_location
>

:end-script:
end script

:terminate-scripts:
exit scripts

:publisher-error:
echo "Error: Failed to start publisher process"
goto terminate-scripts



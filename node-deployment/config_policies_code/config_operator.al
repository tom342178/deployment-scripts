#-----------------------------------------------------------------------------------------------------------------------
# Replication of scripts in config for Operator node - used when node set in debug mode
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/config_policies_code/config_operator.al

on error ignore
if !debug_mode == true then set debug on

:declare-database:
if !debug_mode == true then print "Connect to database(s)"
process !local_scripts/database/deploy_database.al

:declare-node:
if !dbug_mode == true then print "Declare Node policy"
process !local_scripts/policies/cluster_policy.al
process !local_scripts/policies/node_policy.al

:general-configs;
if !debug_mode == true then print "Set scheduler 1"
on error goto scheduler-error
run scheduler 1

on error ignore
process !local_scripts/policies/config_threshold.al

if !debug_mode == true then print "Enable streamer"
on error goto enable-streamer-error
run streamer

if !enable_ha == false then goto run-operator

:enable-ha:
if !debug_mode == true then print "Enable HA"
on error call enable-ha-error
run data distributor
run data consumer where start_date=!start_data

:run-operator:
on error goto run-operator-error
if !debug_mode == true then print "start operator service"
if not !operator_id then
do print "Missing operator ID cannot start operator process"
do goto terminate-scripts

<if !blockchain_source != master then run operator where
    create_table=!create_table and
    update_tsd_info=!update_tsd_info and
    compress_json=!compress_file and
    compress_sql=!compress_sql and
    archive_json=!archive and
    archive_sql=!archive_sql and
    blockchain=!blockchain_source and
    policy=!operator_id and
    threads=!operator_threads>
<else run operator where
    create_table=!create_table and
    update_tsd_info=!update_tsd_info and
    compress_json=!compress_file and
    compress_sql=!compress_sql and
    archive_json=!archive and
    archive_sql=!archive_sql and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads=!operator_threads>

:clean-archive:
on error call clean-archive-error
if !debug_mode == true then print "Set schedule to clean archive"
schedule name=remove_archive and time=1 day and task delete archive where days = !archive_delete

:monitoring-and-local-scripts:
on error ignore
if !debug_mode == true then print "Declare Monitoring & other local scripts"

if !monitor_nodes == true then process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al
if !enable_mqtt == true then process !anylog_path/deployment-scripts/demo-scripts/basic_msg_client.al
if !syslog_monitoring == true then process !anylog_path/deployment-scripts/demo-scripts/syslog.al
if !deploy_local_script == true then process !local_scripts/local_script.al

:end-script:
end script

:terminate-scripts:
exit scripts

:scheduler-error:
print "Failed to set scheduler 1"
goto end-script

:enable-streamer-error:
print "Failed to enable streamer service"
goto end-script

:enable-ha-error:
print "Failed to enable HA for node"
return

:clean-archive-error:
print "Failed to set schedule process for cleaning archives"
return

:run-operator-error:
print "Failed to start operator service"
goto terminate-scripts

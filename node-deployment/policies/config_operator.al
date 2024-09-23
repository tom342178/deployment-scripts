#-----------------------------------------------------------------------------------------------------------------------
# Alternative process for configurating operator - to be used when demonstrating how a node gets deployed.
# :steps:
#   1. declare cluster policy
#   2. declare operator policy
#   3. connect to database(s)
#   4. run scheduler, threashold and streamer
#   5. HA related processes
#   6. start operator
#   7. Enable monitoring andd MQTT
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/node-deployment/policies/config_operator.al

if !debug_mode.int > 0 then set debug on
if !debug_mode.int == 2 then set is_threading = true
set debug off


if !debug_mode.int == 2 then
do set debug interactive
do print "Declare cluster policy"
do set debug on
process !local_scripts/policies/cluster_policy.al

if !debug_mode.int == 2 then
do set debug interactive
do print "Declare node policy"
do set debug on
process !local_scripts/policies/node_policy.al

if !debug_mode.int == 2 then
do set debug interactive
do print "Deploy Database(s)"
do set debug on
process !local_scripts/database/deploy_database.al

if !debug_mode.int == 2 then
do set debug interactive
do print "Enable scheduler 1"
do set debug on
run scheduler 1

if !debug_mode.int == 2 then
do set debug interactive
do print "Set threshold"
do set debug on
<set buffer threshold where
    time=!threshold_time and
    volume=!threshold_volume and
    write_immediate=!write_immediate>

if !debug_mode.int == 2 then
do set debug interactive
do print "Enable streamer"
do set debug on
run streamer

if !enable_ha == true and !debug_mode.int == 2 then
do set debug interactive
do print "Enable distributor"
do set debug on
if !enable_ha == true then run data distributor

if !enable_ha == true and !debug_mode.int == 2 then
do set debug interactive
do print "Enable Consumer"
do set debug on
if !enable_ha == true then run data consumer where start_date=!start_data

if !operator_id and !debug_mode.int == 2 then
do set debug interactive
do print "Start operator process"
do set debug on
if not !operator_id then goto missing-operator-id error
<run operator where
    create_table=!create_table and
    update_tsd_info=!update_tsd_info and
    compress_json=!compress_file and
    compress_sql=!compress_sql and
    archive_json=!archive and
    archive_sql=!archive_sql and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads=!operator_threads>


if !debug_mode.int == 2 then
do set debug interactive
do print "Enable Remove archived files scheduler"
do set debug on
schedule name=remove_archive and time=1 day and task delete archive where days = !archive_delete

if !monitor_nodes == true and !debug_mode.int == 2 then
do set debug interactive
do print "Start start monitoring policy"
do set debug on
do thread !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al
else if !monitor_nodes == true then process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al

if !enable_mqtt == true and !debug_mode.int == 2 then
do set debug interactive
do print "Start MQTT client process"
do set debug on
do thread !anylog_path/deployment-scripts/demo-scripts/basic_msg_client.al
else if !enable_mqtt == true then process !anylog_path/deployment-scripts/demo-scripts/basic_msg_client.al

if !deploy_local_script == true and !debug_mode.int == 2 then
do set debug interactive
do print "Start local / personal script"
do set debug on
do thread !local_scripts/local_script.al
else if !deploy_local_script == true then process !local_scripts/local_script.al

:end-script:
end script

:missing-operator-id:
print "Failed to locate operator ID, cannot declare operator process"
goto end-script

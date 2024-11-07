#-----------------------------------------------------------------------------------------------------------------------
# Replication of scripts in config for Master/Query node - used when node set in debug mode
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/config_policies_code/config_node.al

on error ignore
if !debug_mode.int == 1 then set debug on
else if !debug_mode.int == 2 then set debug interactive

:declare-database:
if !debug_mode.int > 0 then print "Connect to database(s)"
if !debug_mode.int == 2 then thread !local_scripts/database/deploy_database.al
else process !local_scripts/database/deploy_database.al

:declare-policy:
if !dbug_mode.int > 0 then print "Declare Node policy"
if !debug_mode.int == 2 then thread !local_scripts/policies/node_policy.al
else process !local_scripts/policies/node_policy.al

:declare-scheduler:
if !debug_mode.int > 0 then print "Set scheduler 1"
on error goto scheduler-error
run scheduler 1

:monitoring-and-local-scripts:
on error ignore
if !debug_mode.int > 0 then print "Declare Monitoring / Local scripts"

if !monitor_nodes == true and !debug_mode.int == 2 then thread !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al,
else if !monitor_nodes == true then process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al,

if !deploy_local_script == true and !debug_mode.int == 2 then thread !local_scripts/local_script.al
else if !deploy_local_script == true then process !local_scripts/local_script.al

:end-script:
end script

:scheduler-error:
print "Failed to set scheduler 1"
goto end-script
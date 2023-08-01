#--------------------------------------------------------------------------------------------------------------#
# An EdgeX specific node
#   - network configuration
#   - EdgeX policy (for location)
#   - run blockchain sync
#   - operator like node status
#   -
#--------------------------------------------------------------------------------------------------------------#
# process !local_scripts/run_scripts/start_edgex_node.al

on error ignore
:database:
if !deploy_system_query == true then process !local_scripts/deployment_scripts/database/configure_dbms_system_query.al

:scheduler:
process !local_scripts/deployment_scripts/run_scheduler.al

:declare-node-policy:
process !local_scripts/deployment_scripts/policies/edgex_node_policy.al

:monitoring:
process !local_scripts/deployment_scripts/policies/monitoring_node_policy.al
process !local_scripts/deployment_scripts/policies/edgex_monitoring_node_policy.al

:end-script:
end script

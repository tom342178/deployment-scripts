#----------------------------------------------------------------------------------------------------------------------#
# Main for generic scripts
#   -> set directory structure
#   -> set configs
#   -> declare policies
#   -> deploy based on node type
#----------------------------------------------------------------------------------------------------------------------#
# python3 /app/AnyLog-Network/anylog.py process $ANYLOG_PATH/deployment-scripts/deployment-training-based/main.al

on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR
training_scripts = $ANYLOG_PATH/deployment-scripts/deployment-training-based/

on error call work-dirs-error
create work directories

:set-params:
on error ignore
process !training_scripts/set_params.al
process !training_scripts/run_tcp_server.al

:execute-license:
on error call license-error
set license where activation_key=!license_key

:blockchain-seed:
on error call blockchain-seed-error
if !node_type != master then blockchain seed from !ledger_conn

:call-process:
process !training_scripts/generic_policies/generic_monitoring_policy.al
if !node_type == master then process !training_scripts/generic_policies/generic_master_policy.al
if !node_type == query then process !training_scripts/generic_policies/generic_query_policy.al
if !node_type == operator then process !training_scripts/generic_policies/generic_operator_policy.al

:execute-policy:
policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error call config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:get-processes:
on error ignore
get processes
if !enablee_mqtt == true then get msg client

:end-script:
end script

:license-key-error:
print "Failed to enable license key"
return

:blockchain-seed-error:
print "Failed to run blockchain seed"
return

:config-from-policy-error:
print "Failed to configure from policy for node type " !node_type
return




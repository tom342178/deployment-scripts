#----------------------------------------------------------------------------------------------------------------------#
# Main for generic scripts
#   -> set directory structure
#   -> set configs
#   -> declare policies
#   -> execute based on node type
#----------------------------------------------------------------------------------------------------------------------#
# python3 /app/AnyLog-Network/anylog.py process $ANYLOG_PATH/deployment-scripts/scripts/training/main.al

on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

on error call work-dirs-error
create work directories

:set-params:
on error ignore
if $NODE_TYPE then set node_type = $NODE_TYPE
else node_type = generic
if $NODE_NAME then set node_name = $NODE_NAME
else goto missing-node-name

:call-process:
if $NODE_TYPE == master then process !local_scripts/training/generic_policies/mains/master.al

:execute-policy:
policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error call config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:execute-license:
on error call license-error
set license where activation_key=!license_key

:end-script:
end script

:missing-node-name:
print "Missing node name, cannot continue..."
goto end-script

:config-from-policy-error:
print "Failed to configure from policy for node type " !node_type
return

:license-key-error:
print "Failed to enable license key"
return


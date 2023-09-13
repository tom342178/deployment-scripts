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

if !node_type == master then process $ANYLOG_PATH/deployment-scripts/scripts/training/mains/master.al


:get-seed:
on error goto get-seed-error
if !node_type == master then goto set-params

is_blockchain = blockchain test
if !is_blockchain == true or (!is_blockchain == false and !node_type == master) then goto set-params
else if !is_blockchain == false and $LEDGER_CONN then
do blockchain seed $LEDGER_CONN
do seed_count = 1
do goto get-seed
if is !is_blockchain == false and !seed_count then


if !node_type == master then process !local_scripts/training/set_params_for_master.al
else process !local_scripts/training/set_params_from_master.al

if not !license_key then goto missing-license-key
if !node_type != generic and not !company_name then goto missing-company-name

:declare-policies:
on error ignore
process !local_scripts/training/generic_policies/generic_policy.al

# process !local_scripts/training/generic_policies/generic_operator_policy.al
process !local_scripts/training/generic_policies/generic_query_policy.al
# process !local_scripts/training/generic_policies/generic_publisher_policy.al
process !local_scripts/training/generic_policies/generic_monitoring_policy.al

:execute-policy:
policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error call config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:execute-license:
on error call license-error
set license where activation_key=!license_key

:end-script:
end script

:missing-license-key:
print "Missing license key, cannot continue..."
goto end-script

:missing-node-name:
print "Missing node name, cannot continue..."
goto end-script

:missing-company-name:
print "Missing company name, cannot continue..."
goto end-script

:config-from-policy-error:
print "Failed to configure from policy for node type " !node_type
return

:license-key-error:
print "Failed to enable license key"
return

:work-dirs-error:
echo "Failed to create directories"
return

:get-seed-error:
echo "Failed to get seed value from blockchain"
goto declare-policies

:license-error:
print "Failed to set license key..."
goto end-script

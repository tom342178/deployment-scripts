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

:license-key:
on error call license-key-error
if $LICENSE_KEY then set license where activation_key = $LICENSE_KEY

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

on error call work-dirs-error
create work directories

:set-params:
on error ignore
process !local_scripts/training/set_params.al

:get-seed:
on error goto get-seed-error
is_blockchain = blockchain test

is !is_blockchain == false and !seed_count == then goto  get-seed-error
if !is_blockchain == false and !node_type == master then
do ledger_conn = 127.0.0.1:32048
do goto set-params

if !is_blockchain == false then
do blockchain seed !ledger_conn
do seed_count = 1
do goto get-seed

ledger_conn = blockchain get master bring.ip_port

:declare-policies:
process !local_scripts/training/generic_policies/generic_policy.al
process !local_scripts/training/generic_policies/generic_master_policy.al
process !local_scripts/training/generic_policies/generic_operator_policy.al
process !local_scripts/training/generic_policies/generic_query_policy.al
process !local_scripts/training/generic_policies/generic_publisher_policy.al
process !local_scripts/training/generic_policies/generic_monitoring_policy.al

:execute-policy:
policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error call config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:execute-license:
on error call license-error
if not $LICENSE_KEY then
do license_key = blockchain get master bring [*][license]
do set license where activation_key=!license_key

:end-script:
end script

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

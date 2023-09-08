#----------------------------------------------------------------------------------------------------------------------#
# Main for generic scripts
#   -> set directory structure
#   -> set configs
#   -> declare policies
#   -> execute based on node type
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/generic_scripts/main.al

on error ignore
set debug on
set authentication off
set echo queue on

:license-key:
on error call license-key-error
if $LICENSE_KEY then set license where activation_key = $LICENSE_KEY

:directories:
on error ignore
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $ANYLOG_ID_DIR then set id_dir = $ANYLOG_ID_DIR

if $BLOCKCHAIN_DIR then
do set blockchain_dir = $BLOCKCHAIN_DIR
do set blockchain_file = !blockchain_dir/blockchain.json
do set blockchain_new = !blockchain_dir/blockchain.new
do set blockchain_sql = !blockchain_dir/blockchain/blockchain.sql

if $DATA_DIR then  # default: /app/AnyLog-Network/data
do set data_dir = $DATA_DIR
do set archive_dir = !data_dir/archive
do set bkup_dir = !data_dir/bkup
do set blobs_dir = !data_dir/blobs
do set bwatch_dir = !data_dir/bwatch
do set dbms_dir = !data_dir/dbms
do set distr_dir = !data_dir/distr
do set err_dir = !data_dir/error
do set pem_dir = !data_dir/pem
do set prep_dir = !data_dir/prep
do set test_dir = !data_dir/test
do set tmp_dir = !data_dir/tmp
do set watch_dir = !data_dir/watch

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

create work directories

:set-configs:
node_name = anylog-node
node_type = generic
ledger_conn = 127.0.0.1:32048
set default_dbms = test

if $NODE_NAME then set node_name = $NODE_NAME
if $NODE_TYPE then set node_type = $NODE_TYPE
if $LEDGER_CONN then set ledger_conn = $LEDGER_CONN
if $DEFAULT_DBMS then set default_dbms = $DEFAULT_DBMS
if $CONFIG_ID then set config_id = $CONFIG_ID

if !node_type == generic
    anylog_broker_port=32050

:declare-policies:
process !local_scripts/generic_scripts/generic_generic_policy.al
process !local_scripts/generic_scripts/generic_master_policy.al
# process !local_scripts/generic_scripts/generic_operator_policy.al
process !local_scripts/generic_scripts/generic_publisher_policy.al
process !local_scripts/generic_scripts/generic_query_policy.al

:execute-policy:
policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:create-keys:
public_key = get public key where keys_file = node_id
if not !public_key then
do id create keys where password = dummy and keys_file = node_id
do goto create-keys
print !public_key

:end-script:
end script

:config-from-policy-error:
print "Failed to configure from policy for node type " !node_type
goto end-script

:license-key-error:
print "Failed to enable license key"
return


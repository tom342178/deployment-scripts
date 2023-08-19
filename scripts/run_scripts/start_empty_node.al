#-----------------------------------------------------------------------------------------------------------------------
# Prepare an empty node to be used for testing
#   1. set directories
#   2. set license key
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/run_scripts/start_empty_node.al

:directories:
ignore error log
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

if $LICENSE_KEY then set license where activation_key = $LICENSE_KEY
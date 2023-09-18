on error ignore
set debug off
set authentication off
set echo queue on

:prepare-node:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

process !local_scripts/deployment_scripts_new/set_params.al
process !local_scripts/deployment_scripts_new/run_tcp_server.al
blockchain seed from !ledger_conn

set license where activation_key = !license_key

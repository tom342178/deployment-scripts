on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

create work directories

process !local_scripts/training/run_tcp_server.al

ledger_conn = $LEDGER_CONN
#license_key = $LICENSE_KEY

blockchain seed from !ledger_conn

#set license where activation_key = !license_key
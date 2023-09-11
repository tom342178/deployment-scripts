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
on error ignore

:set-configs:
node_type = generic
set default_dbms = test

if $NODE_NAME then set node_name = $NODE_NAME
if $NODE_TYPE in set node_type = $NODE_TYPE
if $LEDGER_CONN then set ledger_conn = $LEDGER_CONN
if $DEFAULT_DBMS then set default_dbms = $DEFAULT_DBMS

:end-script:
end script

:work-dirs-error;
echo "Failed to create directories"
return
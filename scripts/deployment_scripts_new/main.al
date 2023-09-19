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

:blockchain-seed:
reset error log
on error call blockchain-seed-error
blockchain seed from !ledger_conn

:get-license:
master_policy = blockchain get master
if !master_policy then
do license_key = from !master_policy bring [master][license]
do ledger_conn = from !master_policy bring.ip_port

:create-policies:
process !local_scripts/deployment_scripts_new/policies/config_policy.al
set license where activation_key = !license_key

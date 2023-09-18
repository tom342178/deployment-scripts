:prepare-node:
process !local_scripts/deployment_scripts_new/set_params.al
process !local_scripts/deployment_scripts_new/run_tcp_server.al
blockchain seed from !ledger_conn

set license where activation_key = !license_key

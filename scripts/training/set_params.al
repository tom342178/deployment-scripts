on error ignore
set debug off
set authentication off
set echo queue on

:set-configs:
node_type = generic
company_name = New Company
set default_dbms = test

if $NODE_NAME then set node_name = $NODE_NAME
if $NODE_TYPE then set node_type = $NODE_TYPE
if $LEDGER_CONN then set ledger_conn = $LEDGER_CONN
if $DEFAULT_DBMS then set default_dbms = $DEFAULT_DBMS


if !node_type == generic then
do set anylog_server_port = 32548
do set anylog_rest_port = 32549
do set anylog_broker_port = 32550

else if !node_type == master then
do set anylog_server_port = 32048
do set anylog_rest_port = 32049
do ledger_conn = !ip + : + !anylog_server_port

else if !node_type == operator then
do set anylog_server_port = 32148
do set anylog_rest_port = 32149

else if !node_type == query then
do set anylog_server_port = 32348
do set anylog_rest_port = 32349

else if !node_type == publisher then
do set anylog_server_port = 32248
do set anylog_rest_port = 32249



:end-script:
end script
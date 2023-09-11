on error ignore
set debug off
set authentication off
set echo queue on

:set-configs:
node_type = generic
set default_dbms = test

if $NODE_NAME then set node_name = $NODE_NAME
if $NODE_TYPE in set node_type = $NODE_TYPE
if $LEDGER_CONN then set ledger_conn = $LEDGER_CONN
if $DEFAULT_DBMS then set default_dbms = $DEFAULT_DBMS

:end-script:
end script
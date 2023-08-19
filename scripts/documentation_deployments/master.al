#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Part I.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/master.al

:disable-authentication:
# Disable authentication and enable message queue
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)

:set-params:
node_name = Master              # Adds a name to the CLI prompt
company_name="New Company"
anylog_server_port=32048
anylog_rest_port=32049
set tcp_bind=false
set rest_bind=false
tcp_threads=6
rest_threads=6
operator_threads=6
rest_timeout=30
ledger_conn=127.0.0.1:32048

:connect-database:
# connect to default dbms logical database & create ledger table
on error goto connect-dbms-error
connect dbms blockchain where type=sqlite

on error goto ledger-table-error
create table ledger where dbms=blockchain

:configure-network:
on error goto tcp-network-error
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

on error goto rest-network-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

:schedule-processes:
# start scheduler (that service the rule engine)
on error goto schedule1-error
run scheduler 1

# blockchain sync
on error goto blockchain-sync-error
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn

check_policy_count = 0
:check-node-id:
master_id = blockchain get master where name = master-node and company=!company_name
if not !master_id and !check_policy_count == 0  then goto declare-node
if not !master_id and !check_policy_count == 1 then goto declare-node-policy-error

:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"master": {
  "name": "master-node",
  "company": !company_name,
  "ip": !external_ip,
  "local_ip": !ip,
  "port": !anylog_server_port.int,
  "rest_port": !anylog_rest_port.int,
  "cluster": !cluster_id
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
check_policy_count = 1

:confirmation:
print "All blockchain policies and AnyLog services have been initiated"

:end-script:
end script

:connect-dbms-error:
print "Failed to connect to system_operator database"
goto end-script

:ledger-table-error:
print "Failed to create ledger table"
goto end-script

:tcp-network-error:
print "Failed to connect to TCP networking service"
goto end-script

:rest-network-error:
print "Failed to connect to REST networking service"
goto end-script

:schedule1-error:
print "Failed to start `scheduler 1` service"
goto end-script

:blockchain-sync-error:
print "Failed to start blockchain sync process"
goto end-script

:declare-cluster-policy-error:
print "Failed to declare cluster policy on the blockchain"
goto end-script

:declare-node-policy-error:
print "Failed to declare node policy on the blockchain"
goto end-script

:declare-partitions-error:
print "Failed to configure partitions for " + !default_dbms
goto end-script

:buffer-error:
print "Failed to set operator buffer size"
goto end-script

:streamer-error:
print "Failed to run streamer service"
goto end-script

:operator-error:
print "Failed to start operator error to accept data"
goto end-script
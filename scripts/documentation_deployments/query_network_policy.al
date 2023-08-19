#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Policies.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/query_network_policy.al

:disable-authentication:
# Disable authentication and enable message queue
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)

:set-params:
node_name = Query              # Adds a name to the CLI prompt
company_name="New Company"
anylog_server_port=32348
anylog_rest_port=33049
set tcp_bind=false
set rest_bind=false
tcp_threads=6
rest_threads=6
rest_timeout=30
ledger_conn=127.0.0.1:32048

:connect-database:
# connect to system_query using in-memory SQLite
on error goto connect-dbms-error
connect dbms system_query where type=sqlite and memory=true

policy_config_count = 0
:network-id:
on error ignore
network_policy_id = blockchain get config where name = query-network-config and company=!company_name bring [config][id]
if not !network_policy_id and !policy_config_count == 1 then goto network-id-error
else if !network_policy_id then goto execute-policy

:configure-network:
<new_policy = {"config": {
   "name": "query-network-config",
   "company": !company_name,
   "ip": "!external_ip",
   "local_ip": "!ip",
   "port": "!anylog_server_port.int",
   "rest_port": "!anylog_rest_port.int"
}}>

on error goto declare-config-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
policy_config_count = 1
goto network-id

:execute-policy:
on error goto network-id-error
config from policy where id = !network_policy_id

:schedule-processes:
# start scheduler (that service the rule engine)
on error goto schedule1-error
run scheduler 1

# blockchain sync
on error goto blockchain-sync-error
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn

:check-node-id:
node_id = blockchain get query where name = master-node and company=!company_name bring [*][id]
if !node_id then goto confirmation

:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"query": {
  "name": "query-node",
  "company": !company_name,
  "ip": !external_ip,
  "local_ip": !ip,
  "port": !anylog_server_port.int,
  "rest_port": !anylog_rest_port.int
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:confirmation:
print "All blockchain policies and AnyLog services have been initiated"
get processes

:end-script:
end script

:connect-dbms-error:
print "Failed to connect to system_operator database"
goto end-script

:ledger-table-error:
print "Failed to create ledger table"
goto end-script

:network-id-error:
print "Failed to connect to TCP and/or REST service."
goto end-script

:declare-config-policy-error:
print "Failed to declare network config policy on the blockchain"
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

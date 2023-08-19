#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Policies.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/master_policy.al

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
rest_timeout=30
ledger_conn=127.0.0.1:32048
sync_time = "30 seconds"
policy_count = 0

:check-node-id:
node_id = blockchain get master where name = master-node and company=!company_name bring [*][id]
if not !node_id and !policy_count == 1 then goto declare-node-policy-error
else if !node_id then goto execute-policy

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
   "script": [
       'connect dbms blockchain where type=sqlite',
       'create table ledger where dbms=blockchain',
       'run scheduler 1',
       'run blockchain sync where source=master and time=!sync_time seconds and dest=file and connection=!ledger_conn'
   ]
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
policy_count = 1
goto check-node-id

:execute-policy:
on error goto network-id-error
config from policy where id = !network_policy_id

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

:declare-node-policy-error:
print "Failed to declare node policy on the blockchain"
goto end-script

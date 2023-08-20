#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Policies.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/query_policy.al

:disable-authentication:
# Disable authentication and enable message queue
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)

:set-params:
node_name = Query              # Adds a name to the CLI prompt
company_name=My_Company
anylog_server_port=32348
anylog_rest_port=33049
set tcp_bind=false
set rest_bind=false
tcp_threads=6
rest_threads=6
rest_timeout=30
sync_time = "30 seconds"
ledger_conn=127.0.0.1:32048

policy_count = 0
:check-node-id:
node_id = blockchain get master where name = master-node and company=!company_name bring [*][id]
if not !node_id and !policy_count == 1 then goto declare-node-policy-error
else if !node_id then goto execute-policy

:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"query": {
  "name": "query-node",
  "company": !company_name,
  "ip": !external_ip,
  "local_ip": !ip,
  "port": !anylog_server_port.int,
  "rest_port": !anylog_rest_port.int,
   "script": [
       'connect dbms system_query where type=sqlite and memory=true',
       'run scheduler 1',
       'run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn'
   ]
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:execute-policy:
on error goto execute-policy-error
config from policy where id = !node_id

:confirmation:
print "All blockchain policies and AnyLog services have been initiated"
get processes

:end-script:
end script

:declare-node-policy-error:
print "Failed to declare node policy on the blockchain"
goto end-script

:execute-policy-error:
print "Failed to execute query node wth the given configurations"
goto end-script

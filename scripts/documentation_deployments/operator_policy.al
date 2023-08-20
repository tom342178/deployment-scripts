#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Policies.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/operator_policy.al

:disable-authentication:
# Disable authentication and enable message queue
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)

:set-params:
node_name = Operator              # Adds a name to the CLI prompt
company_name=My_Company
set default_dbms = test
anylog_server_port=32148
anylog_rest_port=32149
set tcp_bind=false
set rest_bind=false
tcp_threads=6
rest_threads=6
operator_threads=6
rest_timeout=30
sync_time = 30 seconds
ledger_conn=127.0.0.1:32048

check_policy_count = 0
:check-cluster-id:
on error ignore
cluster_id = blockchain get cluster where name = cluster1 and company=!company_name bring [cluster][id]
if not !cluster_id and !check_policy_count == 1 then goto declare-cluster-policy-error
else if !cluster_id then
do check_policy_count = 0
do goto  check-node-id

:declare-cluster:
<new_policy = {"cluster": {
    "company": !company_name,
    "name": "cluster1"
}}>

on error goto declare-config-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
cluster_id = 1
goto check-cluster-id

:check-node-id:
operator_id = blockchain get operator where name = operator1-node and company=!company_name and cluster=!cluster_id bring [operator][id]
if not !operator_id and !check_policy_count == 1 then goto declare-node-policy-error
else if !operator_id then
do check_policy_count = 0
do goto execute-policy

:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"operator": {
  "name": "operator1-node",
  "company": !company_name,
  "ip": !external_ip,
  "local_ip": !ip,
  "port": !anylog_server_port.int,
  "rest_port": !anylog_rest_port.int,
  "cluster": !cluster_id,
  "script": [
    'connect dbms !default_dbms where type=sqlite',
    'run scheduler 1',
    'run blockchain sync where source=master and time=!sync_time and dest=file and connection=!ledger_conn',
    'partition !default_dbms * using insert_timestamp by 1 day',
    'set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true',
    'run streamer'
  ]
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
check_policy_count = 1
goto check-node-id

:execute-policy:
on error goto execute-policy-error
config from policy where id = !operator_id

:start-operator:
# start operator to accept data coming in
on error goto operator-error
<run operator where
    create_table=true and
    update_tsd_info=true and
    compress_json=true and
    compress_sql=true and
    archive=true and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads = !operator_threads
>

:confirmation:
print "All blockchain policies and AnyLog services have been initiated"
get processes

:end-script:
end script

:declare-cluster-policy-error:
print "Failed to declare cluster policy on the blockchain"
goto end-script

:declare-node-policy-error:
print "Failed to declare node policy on the blockchain"
goto end-script

:execute-policy-error:
print "Failed to execute operator node wth the given configurations"
goto end-script

:operator-error:
print "Failed to start operator error to accept data"
goto end-script

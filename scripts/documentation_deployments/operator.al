#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Part I.md` file in the documentation.
# If a step fails, then an error is printed to screen and scripts stops
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/operator.al

:disable-authentication:
# Disable authentication and enable message queue
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)

:set-directories:
# This is an ENV variable, that's preset as part of the dockerfile - $ANYLOG_PATH = /app
anylog_path = $ANYLOG_PATH

# define the root directory for AnyLog
set anylog home !anylog_path

# This is an ENV variable, that's preset as part of the dockerfile - $LOCAL_SCRIPTS=/app/deployment-scripts/scripts
set local_scripts = $LOCAL_SCRIPTS

# This is an ENV variable, that's preset as part of the dockerfile - $TEST_DIR=/app/deployment-scripts/tests
set test_dir = $TEST_DIR

# create directories (such as blockchain, data/watch. anylog) that are used by the AnyLog node
create work directories

:set-params:
node_name = Operator              # Adds a name to the CLI prompt
company_name="New Company"
set default_dbms = test
anylog_server_port=32148
anylog_rest_port=32149
set tcp_bind=false
set rest_bind=false
tcp_threads=6
rest_threads=6
operator_threads=6
rest_timeout=30
ledger_conn=127.0.0.1:32048

:connect-database:
# connect to defaault dbms logical database
on error goto connect-dbms-error
connect dbms !default_dbms where type=sqlite

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
run blockchain sync where source=operator and time="30 seconds" and dest=file and connection=!ledger_conn

check_policy_count = 0
:check-cluster-id:
on error ignore
cluster_id = blockchain get cluster where name = cluster1 and company=!company_name
if not !cluster_id and !check_policy_count == 0  then goto declare-cluster
else if not !cluster_id and !check_policy_count == 1 then goto declare-cluster-policy-error
else if !cluster_id then
do check_policy_count = 0
do goto  check-node-id

:declare-cluster:
<new_policy = {"cluster": {
    "company": !company_name,
    "name": "cluster1"
}}>

on error goto declare-cluster-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and operator=!ledger_conn
cluster_id = 1
goto check-cluster-id

:check-node-id:
operator_id = blockchain get operator where name = operator1-node and company=!company_name and cluster=!cluster_id
if not !operator_id and !check_policy_count == 0  then goto declare-node
if not !operator_id and !check_policy_count == 1 then goto declare-node-policy-error
else if !operator_id then
do goto start-operator

:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"operator": {
  "name": "operator1-node",
  "company": !company_name,
  "ip": !external_ip,
  "local_ip": !ip,
  "port": !anylog_server_port.int,
  "rest_port": !anylog_rest_port.int
}}>

on error goto declare-node-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and operator=!ledger_conn
check_policy_count = 1

:declare-partitions:
# declare partitions of the node - this step is optional, but provides better query performance
on error goto declare-partitions-error
partition !default_dbms * using insert_timestamp by 1 day

:start-operator:
# buffer thresholds size and time
on error goto buffer-error
set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true

# Enable the streamer service - to writes streaming data to files
on error goto streamer-error
run streamer

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

:end-script:
end script

:connect-dbms-error:
print "Failed to connect to system_operator database"
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
#-----------------------------------------------------------------------------------------------------------------------
# Script is based on `Network Setup - Policies.md` file in the documentation
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/documentation_deployments/master_configuration.al

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

:blockchain-database:
# Declare a database to service the metadata table (the ledger table)
on error goto connect-dbms-error
connect dbms blockchain where type=sqlite

on error goto create-table-error
create table ledger where dbms=blockchain

check_policy_count = 0
:check-policy:
# check if network policy is on the blockchain
on error ignore
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id]
if not !policy_id and !check_policy_count == 0 then goto declare-network-policy
else if not !policy_id and !check_policy_id == 1 then goto declare-network-policy-error
else goto execute-policy

:declare-network-policy:
# create configuration policy to be used to connect to the network
on error ignore
<new_policy = {"config": {
   "name": "anylog-master-network-configs",
   "company": !company_name,
   "ip": "!external_ip",
   "local_ip": "!ip",
   "port": "!anylog_server_port.int",
   "rest_port": "!anylog_rest_port.int"
}}>

on error goto declare-network-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
check_policy_count = 1

:execute-policy:
on error goto execute-policy-error
config from policy where id = !policy_id

:schedule-processes:
# start scheduler (that service the rule engine)
on error goto schedule1-error
run scheduler 1

# blockchain sync
on error goto blockchain-sync-error
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn


:declare-node:
on error ignore
# if TCP bind is false, then state both external and local IP addresses
<new_policy = {"master": {
  "name": "master-node",
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
print "All blockchain policies and AnyLog servicces have been initiated"

:end-script:
end script

:connect-dbms-error:
print "Failed to connect to blockchain database"
goto end-script

:create-table-error:
print "Failed to create ledger table on blockchain database"
goto end-script

:declare-network-policy-error:
print "Failed to declare network configuration on the blockchain"
goto end-script

:execute-policy-error:
print "Failed to connect to TCP/REST network services"
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

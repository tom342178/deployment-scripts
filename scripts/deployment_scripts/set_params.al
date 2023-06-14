#-----------------------------------------------------------------------------------------------------------------------
# The following takes the environment variables and converts them into AnyLog variables
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/set_params.al

on error call set-params-error

if $LICENSE_KEY then set license_key = $LICENSE_KEY

:node-types:
# node type
set deploy_ledger = false
set deploy_operator = false
set deploy_publisher = false
set deploy_query = false

if $NODE_TYPE == ledger or $NODE_TYPE == master or $NODE_TYPE == standalone or $NODE_TYPE == standalone-publisher then set deploy_ledger = true
if $NODE_TYPE == operator or $NODE_TYPE == standalone then set deploy_operator = true
if $NODE_TYPE == publisher or $NODE_TYPE == standalone-publisher  then set deploy_publisher = true
if $NODE_TYPE == query then set deploy_query = true

if !deploy_operator == true  and !deploy_publisher == true then
do echo "Notice: Unable to support both operator & publisher on the same node. Disabling Publisher"
do set deploy_publisher = false

:general-params:
hostname = get hostname
node_name = anylog-node
company_name = "New Company"
country = "Unknown"
state = "Unknown"
city = "Unknown"

if $NODE_NAME then node_name = $NODE_NAME
if $COMPANY_NAME then company_name = $COMPANY_NAME
if $LOCATION then loc = $LOCATION
if $COUNTRY then country = $COUNTRY
if $STATE then state = $STATE
if $CITY then city = $CITY

#----------------------------------------------------------#
# Sample output from cURL request
#{
#  "ip": "24.23.250.144",
#  "hostname": "c-24-23-250-144.hsd1.ca.comcast.net",
#  "city": "San Mateo",
#  "state": "California",
#  "country": "US",
#  "loc": "37.5630,-122.3255",
#  "org": "AS33651 Comcast Cable Communications, LLC",
#  "postal": "94401",
#  "timezone": "America/Los_Angeles",
#  "readme": "https://ipinfo.io/missingauth"
#}
#----------------------------------------------------------#
on error ignore
if not !loc then info = rest get where url = https://ipinfo.io/json
if !info then
do loc = from !info bring [loc]
do country = from !info bring [country]
do state = from !info bring [region]
do city = from !info bring [city]

if not !info and not !loc then loc = 0.0, 0.0
if not !info and not !country then country = Unknown
if not !info and not !state then state = Unknown
if not !info and not !city then city = Unknown

:networking:
on error call set-params-error
# networking params
anylog_server_port=32048
anylog_rest_port=32049

if $ANYLOG_SERVER_PORT then anylog_server_port  = $ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then anylog_rest_port = $ANYLOG_REST_PORT
if $ANYLOG_BROKER_PORT then anylog_broker_port = $ANYLOG_BROKER_PORT

if $POLICY_BASED_NETWORKING then set policy_based_networking = $POLICY_BASED_NETWORKING
if !policy_based_networking != true and  !policy_based_networking != false then  set policy_based_networking = false

# whether to setup networking based on a (generic) configuration policy - good for both REST and other nodes
if $CONFIG_POLICY then set config_policy=$CONFIG_POLICY
if !config_policy != true and !config_policy != false then set config_policy=true

if $EXTERNAL_IP then set external_ip = $EXTERNAL_IP
if $LOCAL_IP then set ip = $LOCAL_IP
if $OVERLAY_IP then set overlay_ip = $OVERLAY_IP
if $PROXY_IP then proxy_ip=$PROXY_IP

# Kubernetes service name - used in stead of local IP on the blockchain if set / no overlay IP
if $KUBERNETES_SERVICE_IP then set kubernetes_service_ip = $KUBERNETES_SERVICE_IP

# if a user doesn't set TCP bind, assume true unless external != local IP adddress
if $TCP_BIND then set tcp_bind = $TCP_BIND
if !tcp_bind != true and !tcp_bind != false and !overlay_ip then set tcp_bind = true
else if !tcp_bind != true and !tcp_bind != false and !external_ip == !ip then  set tcp_bind = true
else if !tcp_bind != true and !tcp_bind != false then set tcp_bind = false

ledger_conn = !ip + ":" + !anylog_server_port
if $LEDGER_CONN then ledger_conn = $LEDGER_CONN

if !tcp_bind == false then goto advanced-networking

ledger_ip = python !ledger_conn.split(":")[0]
ledger_port = python !ledger_conn.split(":")[1]
if (!ledger_ip == 127.0.0.1 or !ledger_ip == localhost) and !overlay_ip then ledger_conn = !overlay_ip + ":" + !ledger_port
if (!ledger_ip == 127.0.0.1 or !ledger_ip == localhost) and not !overlay_ip then ledger_conn = !ip + ":" + !ledger_port

:advanced-networking:
# Advanced Networking Configurations
if $NODE_TYPE == rest  or !policy_based_networking == false and $TCP_THREADS then tcp_threads=$TCP_THREADS
if $NODE_TYPE == rest  or !policy_based_networking == false and !tcp_threads < 1 then tcp_threads=1
if $NODE_TYPE == rest  or !policy_based_networking == false and not !tcp_threads then tcp_threads=6

if $REST_BIND then set rest_bind = $REST_BIND
if !rest_bind != true and !rest_bind != false then set rest_bind = false

if $NODE_TYPE == rest  or !policy_based_networking == false and $REST_THREADS then  rest_threads = $REST_THREADS
if $NODE_TYPE == rest  or !policy_based_networking == false and !rest_threads < 1 then rest_threads=1
if $NODE_TYPE == rest  or !policy_based_networking == false and not !rest_threads then rest_threads = 6

if $NODE_TYPE == rest  or !policy_based_networking == false and  $REST_TIMEOUT then set rest_timeout = $REST_TIMEOUT
if $NODE_TYPE == rest  or !policy_based_networking == false and !rest_timeout < 0 then rest_timeout = 0
if $NODE_TYPE == rest  or !policy_based_networking == false and not !rest_timeout then rest_timeout = 20

rest_ssl = false # need to implement REST SSL code

if $BROKER_BIND then set broker_bind = $BROKER_BIND
if !broker_bind != true and !broker_bind != false then set broker_bind = false

if $NODE_TYPE == rest  or !policy_based_networking == false and $BROKER_THREADS then  broker_threads = $BROKER_THREADS
if $NODE_TYPE == rest  or !policy_based_networking == false and !broker_threads < 1 then broker_threads=1
if $NODE_TYPE == rest  or !policy_based_networking == false and not !broker_threads then broker_threads = 6


if $CONFIG_POLICY_NAME then
do config_policy_name = $CONFIG_POLICY_NAME
do goto authentication
if not $CONFIG_POLICY_NAME and !overlay_ip then goto config-policy-name-overlay
if not $CONFIG_POLICY_NAME and not !overlay_ip then goto config-policy-name

:config-policy-name: 
if $NODE_TYPE == rest then config_policy_name = rest-configs
else if $NODE_TYPE == master then config_policy_name = master-configs
else if $NODE_TYPE == operator then config_policy_name = operator-configs
else if $NODE_TYPE == publisher then config_policy_name = publisher-configs
else if $NODE_TYPE == query then config_policy_name = query-configs
else if $NODE_TYPE == standalone then config_policy_name = standalone-configs
else if $NODE_TYPE == standalone-publisher then config_policy_name = standalone-publisher-configs
else config_policy_name = network-confiig-policy
goto authentication

:config-policy-name-overlay:
if $NODE_TYPE == rest then config_policy_name = rest-overlay-configs
else if $NODE_TYPE == master then config_policy_name = master-overlay-configs
else if $NODE_TYPE == operator then config_policy_name = operator-overlay-configs
else if $NODE_TYPE == publisher then config_policy_name = publisher-overlay-configs
else if $NODE_TYPE == query then config_policy_name = query-overlay-configs
else if $NODE_TYPE == standalone then config_policy_name = standalone-overlay-configs
else if $NODE_TYPE == standalone-publisher then config_policy_name = standalone-publisher-overlay-configs
else config_policy_name = network-confiig-policy-overlay

:authentication:
# Authentication information
if $ENABLE_AUTH then set enable_auth = $ENABLE_AUTH
if !enable_auth != true and !enable_auth != false then set enable_auth = false

if $ENABLE_REST_AUTH then set enable_rest_auth = $ENABLE_REST_AUTH
if !enable_rest_auth != true and !enable_rest_auth != false then set enable_rest_auth = false

if $NODE_PASSWORD then set node_password = $NODE_PASSWORD
if $USER_NAME then user_name = $USER_NAME
if $USER_PASSWORD then user_password = $USER_PASSWORD
if $USER_TYPE then user_type = $USER_TYPE

if $ROOT_USER then root_user = $ROOT_USER
if not !root_user then root_user = admin

if $ROOT_PASSWORD then root_password = $ROOT_PASSWORD

:database:
# Database params
db_type = sqlite
if !deploy_operator then set default_dbms=test

if $DB_TYPE then db_type = $DB_TYPE
if !db_type != psql and !db_type != sqlite then db_type = sqlite

if !db_type != sqlite then
do if $DB_USER then db_user = $DB_USER
do if $DB_PASSWD then set db_passwd = $DB_PASSWD
do if $DB_IP then db_ip = $DB_IP
do if $DB_PORT then db_port = $DB_PORT

if !deploy_operator == true and $DEFAULT_DBMS then default_dbms = $DEFAULT_DBMS

set autocommit = $AUTOCOMMIT
if !autocommit != true and !autocommit != false then set autocommit=false

if !deploy_query == true then set deploy_system_query = true
else if $DEPLOY_SYSTEM_QUERY == true or $DEPLOY_SYSTEM_QUERY == false  then set deploy_system_query=$DEPLOY_SYSTEM_QUERY
else set deploy_system_query = false

if $MEMORY then !memory = $MEMORY
if !memory != true and !memory != false then set memory = false

if $NOSQL_ENABLE then set enable_nosql=$NOSQL_ENABLE
if !enable_nosql != true and !enable_nosql != false then enable_nosql=false

nosql_type = mongo
if $NOSQL_TYPE then set nosql_type = $NOSQL_TYPE
nosql_ip = 127.0.0.1
if $NOSQL_IP then nosql_ip = $NOSQL_IP
nosql_port = 27017
if $NOSQL_PORT then nosql_port = $NOSQL_PORT

if $NOSQL_USER then nosql_user = $NOSQL_USER
if $NOSQL_PASSWD then nosql_passwd = $NOSQL_PASSWD

if $NOSQL_BLOBS_DBMS then set blobs_dbms = $NOSQL_BLOBS_DBMS
if !blobs_dbms != true and !blobs_dbms != false then set blobs_dbms=false
if $NOSQL_BLOBS_FOLDER then set blobs_folder = $NOSQL_BLOBS_FOLDER
if !blobs_folder != true and !blobs_folder != false then set blobs_folder=true
if $NOSQL_BLOBS_COMPRESS then set blobs_compress = $NOSQL_BLOBS_COMPRESS
if !blobs_compress != true and !blobs_compres != false then set blobs_compress=true
if $NOSQL_BLOBS_REUSE then set blobs_reuse = $NOSQL_BLOBS_REUSE
if !blobs_reuse != true and !blobs_reuse != false then set blobs_reuse = true


:settings:
# settings
operator_threads = 1
query_pool = 3

if $OPERATOR_THREADS then operator_threads = $OPERATOR_THREADS
if !operater_threads < 1 then operator_threads = 1
if $QUERY_POOL then query_pool = $QUERY_POOL
if $QUERY_POOL and query_pool < 3 then query_pool = 3

# blockchain sync
sync_time="30 seconds"
blockchain_source=master
set blockchain_destination = file

if $SYNC_TIME then sync_time = $SYNC_TIME
if $SOURCE then blockchain_source=$SOURCE
if $DESTINATION then set blockchain_destination=$DESTINATION

:operator-settings:
# Operator specific params & partitions
enable_partitions=true
cluster_name = !company_name
table_name=*
partition_column = insert_timestamp
partition_interval = "14 days"
partition_keep = 6 # keep about 3 months of data
partition_sync = "1 day"

if $ENABLE_PARTITIONS then enable_partitions=$ENABLE_PARTITIONS
if $CLUSTER_NAME then cluster_name = $CLUSTER_NAME
if $TABLE_NAME then table_name=$TABLE_NAME
if $PARTITION_COLUMN then partition_column = $PARTITION_COLUMN
if $PARTITION_INTERVAL then partition_interval = $PARTITION_INTERVAL
if $PARTITION_KEEP then partition_keep = $PARTITION_KEEP
if $PARTITION_SYNC then partition_sync = $PARTITION_SYNC

if $MEMBER then member = $MEMBER

:other-settings:
if $ENABLE_MQTT then set enable_mqtt = $ENABLE_MQTT
if !enable_mqtt != true and !enable_mqtt != false then set enable_mqtt = false

if $DEPLOY_LOCAL_SCRIPT then set deploy_local_script=$DEPLOY_LOCAL_SCRIPT
if !deploy_local_script != true and !deploy_local_script != false then set deploy_local_script = false

# run operator / publisher configs
if $CREATE_TABLE then set create=$CREATE_TABLE
if !create_table != true and !create_table != false then set create_table = true

if $UPDATE_TSD_INFO then set update_tsd_info=$UPDATE_TSD_INFO
if !update_tsd_info != true and !update_tsd_info != false then set update_tsd_info=true

if $ARCHIVE then set archive=$ARCHIVE
if !archive != true and !archive != false then set archive=true

if $DISTRIBUTOR then set distributor=$DISTRIBUTOR
if !distributor != true and !distributor != false then set distributor=true

if $COMPRESS_FILE then set compress_file = $COMPRESS_FILE
if !compress_file != true and !compress_file != false then set compress_file = true

if $MOVE_JSON then set move_json = $MOVE_JSON
if !move_json != true and !move_json != false then set move_json = true

if $DBMS_FILE_LOCATION then dbms_file_location = $DBMS_FILE_LOCATION
else dbms_file_location = file_name[0]

if $PUBLISHER_COMPRESS_FILE then set publisher_compress_file = $PUBLISHER_COMPRESS_FILE
if !publisher_compress_file != true and !publisher_compress_file != false then publisher_compress_file=false

if $TABLE_FILE_LOCATION then table_file_location = $TABLE_FILE_LOCATION
else table_file_location = file_name[1]

if $ENABLE_HA then set enable_ha = $ENABLE_HA
if !enable_ha != true and !enable_ha != false then set enable_ha = false

if !enable_ha == true then
do ha_start_date = -30d
do if $START_DATE then ha_start_date = $START_DATE

set write_immediate = true
if $WRITE_IMMEDIATE then set write_immediate = $WRITE_IMMEDIATE
if !write_immediate != true and !write_immediate != false then set write_immediate = true

threshold_time = 60 seconds
threshold_volume = 10KB
if $THRESHOLD_TIME then threshold_time = $THRESHOLD_TIME
if $THRESHOLD_VOLUME then threshold_volume = $THRESHOLD_VOLUME

monitor_nodes = false # whether to monitor node(s)  or not  
monitor_node = query  # which node type to send monitoring information to 
monitor_node_company = "New Company" # company node is associted wth
if $MONITOR_NODES then monitor_nodes = $MONITOR_NODES
if $MONITOR_NODE then monitor_nodes = $MONITOR_NODE 
if $MONITOR_NODE_COMPANY then monitor_node_company = $$MONITOR_NODE_COMPANY


:end-script:
end script

:set-params-error:
echo "Error: Failed to configure one or more parameters"
return



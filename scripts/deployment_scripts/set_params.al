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
anylog_server_port=32548
anylog_server_port=32549
tcp_bind = false
rest_bind = false
broker_bind = false

if $ANYLOG_SERVER_PORT then anylog_server_port  = $ANYLOG_SERVER_PORT
else if $NODE_TYPE == master or $NODE_TYPE == standalone or $NODE_TYPE == standalone-publisher then anylog_server_port=32048
else if $NODE_TYPE == operator then anylog_server_port=32148
else if $NODE_TYPE == publisher then anylog_server_port=32248
else if $NODE_TYPE == query then anylog_server_port=32348
if $TCP_BIND == true or $TCP_BIND == True or $TCP_BIND == TRUE then set tcp_bind = true

if $ANYLOG_REST_PORT then anylog_rest_port = $ANYLOG_REST_PORT
else if $NODE_TYPE == master or $NODE_TYPE == standalone or $NODE_TYPE == standalone-publisher then anylog_server_port=32049
else if $NODE_TYPE == operator then anylog_server_port=32149
else if $NODE_TYPE == publisher then anylog_server_port=32249
else if $NODE_TYPE == query then anylog_server_port=32349
else if $ANYLOG_SERVER_PORT then anylog_server_port  = $ANYLOG_SERVER_PORT

if $REST_BIND == true or $REST_BIND == True or $REST_BIND == TRUE then set rest_bind = true

if $ANYLOG_BROKER_PORT then anylog_broker_port = $ANYLOG_BROKER_PORT
if $BROKER_BIND == true or $BROKER_BIND == True or $BROKER_BIND == TRUE then broker_bind = true

if $EXTERNAL_IP then set external_ip = $EXTERNAL_IP
if $LOCAL_IP then set ip = $LOCAL_IP
if $OVERLAY_IP then set overlay_ip = $OVERLAY_IP
if $PROXY_IP then proxy_ip=$PROXY_IP

# Kubernetes service name - used instead of local IP on the blockchain if set / no overlay IP
if $KUBERNETES_SERVICE_IP then set kubernetes_service_ip = $KUBERNETES_SERVICE_IP

:network-config-policy:
# network configuration policy
policy_based_networking = true
config_policy=true
tmp_name = python !node_name.replace(" ","-").replace("_", "-")
config_policy_name = !tmp_name + "-config"

if !overlay_ip then config_policy_name = !tmp_name + "-overlay-config"

if $POLICY_BASED_NETWORKING == false or $POLICY_BASED_NETWORKING == False or $POLICY_BASED_NETWORKING == FALSE then set policy_based_networking = false
if $CONFIG_POLICY == false or $CONFIG_POLICY == False or $CONFIG_POLICY == FALSE then set config_policy = false
if $CONFIG_POLICY_NAME then config_policy_name = $CONFIG_POLICY_NAME

:advanced-networking:
tcp_threads=6
rest_threads=6
rest_timeout=30
broker_threads=6

if $TCP_THREADS then
do tcp_threads = $TCP_THREADS
do if !tcp_threads.int < 1  then tcp_threads = 1

if $REST_THREADS then
do rest_threads = $REST_THREADS
do if !rest_threads.int < 1 then rest_threads = 1
if $REST_TIMEOUT then
do rest_timeout=$REST_TIMEOUT
do if !rest_timeout.int < 0 then rest_timeout=0

if $BROKER_THREADS then
do broker_threads = $BROKER_THREADS
do if !broker_threads.int < 1 then broker_threads = 1

:authentication:
# Authentication information
enable_auth = false
enable_rest_auth = false

if $ENABLE_AUTH == true or $ENABLE_AUTH == True or $ENABLE_AUTH == TRUE then set enable_auth = true
if $ENABLE_REST_AUTH == true or $ENABLE_REST_AUTH == True or $ENABLE_REST_AUTH == TRUE then set enable_auth = true

:database:
# Database params
db_type = sqlite
autocommit = true
set deploy_system_query = false

if $DB_TYPE then db_type = $DB_TYPE
if !db_type != sqlite and !db_type != psql then
do echo "Invalidate database type " + !db_type
do terminate scripts

if !deploy_operator then set default_dbms=test
if !deploy_operator == true and $DEFAULT_DBMS then default_dbms = $DEFAULT_DBMS

if !db_type != sqlite then
do if $DB_USER then db_user = $DB_USER
do if $DB_PASSWD then set db_passwd = $DB_PASSWD
do if $DB_IP then db_ip = $DB_IP
do if $DB_PORT then db_port = $DB_PORT

if $AUTOCOMMIT == false or $AUTOCOMMIT == False or $AUTOCOMMIT == FALSE then set autocommit = false

if !deploy_query == true or $DEPLOY_SYSTEM_QUERY == true or $DEPLOY_SYSTEM_QUERY == True or $DEPLOY_SYSTEM_QUERY == TRUE  then
do set deploy_system_query = true
do memory = true
do if $MEMORY == false or $MEMORY == False or $MEMORY == FALSE then memory=false


:database-mongodb:
set enable_nosql = false
if $NOSQL_ENABLE == true or $NOSQL_ENABLE == True or $NOSQL_ENABLE == TRUE then set enable_nosql = true

nosql_type = mongo
nosql_ip = 127.0.0.1
nosql_port = 27017
set blobs_dbms = false
set blobs_folder = true
set blobs_compress = true
set blobs_reuse = true

if $NOSQL_TYPE then set nosql_type = $NOSQL_TYPE
if $NOSQL_IP then nosql_ip = $NOSQL_IP
if $NOSQL_PORT then nosql_port = $NOSQL_PORT
if $NOSQL_USER then nosql_user = $NOSQL_USER
if $NOSQL_PASSWD then nosql_passwd = $NOSQL_PASSWD

if $NOSQL_BLOBS_DBMS == true or $NOSQL_BLOBS_DBMS == True or $NOSQL_BLOBS_DBMS == TRUE  then set blobs_dbms = true
if $NOSQL_BLOBS_FOLDER == false or $NOSQL_BLOBS_FOLDER == False or $NOSQL_BLOBS_FOLDER == FALSE  then set blobs_folder = false
if $NOSQL_BLOBS_COMPRESS == false or $NOSQL_BLOBS_COMPRESS == False or $NOSQL_BLOBS_COMPRESS == FALSE  then set blobs_folder = false
if $NOSQL_BLOBS_REUSE == false or $NOSQL_BLOBS_REUSE == False or $NOSQL_BLOBS_REUSE == FALSE  then set blobs_folder = false

:settings:
# settings
operator_threads = 1
query_pool = 3

if $OPERATOR_THREADS then
do operator_threads = $OPERATOR_THREADS
do if !operator_threads.int < 1 then operator_threads = 1
if $QUERY_POOL then
do query_pool = $QUERY_POOL
do !query_pool.int < 3 then query_pool = 3

:blockchain:
ledger_conn = !ip + ":" + !anylog_server_port
if $LEDGER_CONN then ledger_conn = $LEDGER_CONN

ledger_ip = python !ledger_conn.split(":")[0]
ledger_port = python !ledger_conn.split(":")[1]
if (!ledger_ip == 127.0.0.1 or !ledger_ip == localhost) and !overlay_ip then ledger_conn = !overlay_ip + ":" + !ledger_port
if (!ledger_ip == 127.0.0.1 or !ledger_ip == localhost) and not !overlay_ip then ledger_conn = !ip + ":" + !ledger_port

# blockchain sync
sync_time="30 seconds"
blockchain_source=master
set blockchain_destination = file

if $SYNC_TIME then sync_time = $SYNC_TIME
if $SOURCE then blockchain_source=$SOURCE
if $DESTINATION then set blockchain_destination=$DESTINATION

:operator-settings:
# Operator specific params & partitions
enable_partitions=false
cluster_name = python !company_name.replace(" ","-").replace("_", "-")
table_name=*
partition_column = insert_timestamp
partition_interval = "14 days"
partition_keep = 6 # keep about 3 months of data
partition_sync = "1 day"

if $ENABLE_PARTITIONS == true or $ENABLE_PARTITIONS == True or $ENABLE_PARTITIONS == TRUE then enable_partitions=true
if $CLUSTER_NAME then cluster_name = $CLUSTER_NAME
if $TABLE_NAME then table_name=$TABLE_NAME
if $PARTITION_COLUMN then partition_column = $PARTITION_COLUMN
if $PARTITION_INTERVAL then partition_interval = $PARTITION_INTERVAL
if $PARTITION_KEEP then partition_keep = $PARTITION_KEEP
if $PARTITION_SYNC then partition_sync = $PARTITION_SYNC

if $MEMBER then member = $MEMBER

:mqtt:
set enable_mqtt = false
mqtt_broker = driver.cloudmqtt.com
mqtt_port = 18785
mqtt_user = ibglowct
mqtt_password = MSY4e009J7ts
mqtt_topic = anylogedgex-demo
set mqtt_log = false
set mqtt_dbms = test
if !default_dbms then set mqtt_dbms = !default_dbms
mqtt_table = "bring [sourceName]"
mqtt_timestamp_column = now
mqtt_value_column_type = float
mqtt_value_column = "bring [readings][][value]"

if $ENABLE_MQTT == true or $ENABLE_MQTT == True or $ENABLE_MQTT == TRUE then set enable_mqtt = true
if $MQTT_LOG == true or $MQTT_LOG == True or $MQTT_LOG == TRUE then set mqtt_log = true
if $MQTT_BROKER then mqtt_broker=$MQTT_BROKER
if $MQTT_PORT then mqtt_port=$MQTT_PORT
if $MQTT_USER then mqtt_user=$MQTT_USER
if $MQTT_PASSWD then mqtt_passwd=$MQTT_PASSWD
if $MQTT_TOPIC then mqtt_topic=$MQTT_TOPIC
if $MQTT_DBMS then mqtt_dbms=$MQTT_DBMS
if $MQTT_TABLE then mqtt_table=$MQTT_TABLE
if $MQTT_TIMESTAMP_COLUMN then mqtt_timestamp_column=$MQTT_TIMESTAMP_COLUMN
if $MQTT_VALUE_COLUMN_TYPE then mqtt_value_column_type=$MQTT_VALUE_COLUMN_TYPE
if $MQTT_VALUE_COLUMN then mqtt_value_column=$MQTT_VALUE_COLUMN

:other-settings:
set deploy_local_script = false
set create_table = true
set update_tsd_info = true
set archive = true
set distributor = true
set compress_file = true
set move_json = true
set publisher_compress_file = true
set write_immediate = true
set enable_ha = false

dbms_file_location = file_name[0]
table_file_location = file_name[1]
threshold_time = 60 seconds
threshold_volume = 10KB

set monitor_nodes = false
set monitor_node = query
monitor_node_company = !company_name

if $DEPLOY_LOCAL_SCRIPT == true or $DEPLOY_LOCAL_SCRIPT == True or $DEPLOY_LOCAL_SCRIPT == TRUE then set deploy_local_script=true
if $CREATE_TABLE == false or $CREATE_TABLE == False or $CREATE_TABLE == FALSE then set create_table=false
if $UPDATE_TSD_INFO == false or $UPDATE_TSD_INFO == False or $UPDATE_TSD_INFO == FALSE then set update_tsd_info=false
if $ARCHIVE == false or $ARCHIVE == False or $ARCHIVE == FALSE then set archive=false
if $DISTRIBUTOR == false or $DISTRIBUTOR == False or $DISTRIBUTOR == FALSE then set distributor=false
if $COMPRESS_FILE == false or $COMPRESS_FILE == False or $COMPRESS_FILE == FALSE then set compress_file=false
if $MOVE_JSON == false or $MOVE_JSON == False or $MOVE_JSON == FALSE then set move_json=false
if $PUBLISHER_COMPRESS_FILE == false or $PUBLISHER_COMPRESS_FILE == False or $PUBLISHER_COMPRESS_FILE == FALSE then set publisher_compress_file=false
if $WRITE_IMMEDIATE == false or $WRITE_IMMEDIATE == False or $WRITE_IMMEDIATE == FALSE then set write_immediate=false

if $ENABLE_HA == true or $ENABLE_HA == True or $ENABLE_HA == TRUE then
do set enable_ha=true
do ha_start_date = -30d
do if $START_DATE then ha_start_date = $START_DATE

if $DBMS_FILE_LOCATION then dbms_file_location = $DBMS_FILE_LOCATION
if $TABLE_FILE_LOCATION then table_file_location = $TABLE_FILE_LOCATION

if $THRESHOLD_TIME then threshold_time = $THRESHOLD_TIME
if $THRESHOLD_VOLUME then threshold_volume = $THRESHOLD_VOLUME

if $MONITOR_NODES == true or $MONITOR_NODES == True or $MONITOR_NODES == TRUE then set monitor_nodes=true
if $MONITOR_NODE then set monitor_node = $MONITOR_NODE
if $MONITOR_NODE_COMPANY then monitor_node_company = $MONITOR_NODE_COMPANY


:end-script:
end script

:set-params-error:
echo "Error: Failed to configure one or more parameters"
return



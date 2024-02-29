#-----------------------------------------------------------------------------------------------------------------------
# The following takes the environment variables and converts them into AnyLog variables
#   --> required params (ex. node_type, node_name, company_name, license)
#   --> general params (ex. hostname, location)
#   --> networking (ex. binding, ports, port thread count, REST timeout)
#   --> authentication (ex. enabling) - credentials are in authentication scripts
#   --> sql-database (ex. type, credentials, enabling system_query)
#   --> nosql-database (ex. type and credentials)
#   --> blockchain (ex. sync time, ledger_conn, source and destination)
#   --> operator-settings (ex. partitioning data, cluster name, operator member ID)
#   --> operator-ha (ex. enable ha and how far back)
#   --> mqtt (ex. enable, broker credential information, data mapping)
#   --> node-monitoring (ex. enable monitoring, node that receives monitoring and company associated with that node)
#   --> settings (ex. streaming speed / size, deploy local/personalized script)
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/set_params.al
on error ignore


:required-params:
if $NODE_TYPE then set node_type = $NODE_TYPE
else goto missing-node-type
if $NODE_NAME then
do set node_name = $NODE_NAME
do set node name !node_name
else goto missing-node-name

if $LICENSE_KEY then license_key=$LICENSE_KEY
else goto missing-license-key

if $COMPANY_NAME then company_name = $COMPANY_NAME
else goto missing-company-name

if $LEDGER_CONN then ledger_conn=$LEDGER_CONN
else goto missing-ledger-conn

:general-params:
hostname = get hostname
loc = 0.0, 0.0
country = Unknown
state = Unknown
city = Unknown

loc_info = rest get where url = https://ipinfo.io/json
if !loc_info then
do loc = from !loc_info bring [loc]
do country = from !loc_info bring [country]
do state = from !loc_info bring [state]
do city = from !loc_info bring [city]


:networking:
config_name = !node_type.name + - + !company_name.name + -configs
tcp_bind = false
tcp_threads=6
rest_bind = false
rest_threads=6
rest_timeout=30
broker_bind = false
broker_threads=6

if !node_type == master then
do anylog_server_port = 32048
do anylog_rest_port = 32048

if !node_type == operator then
do anylog_server_port = 32148
do anylog_rest_port = 32148

if !node_type == publisher then
do anylog_server_port = 32248
do anylog_rest_port = 32248

if !node_type == query then
do anylog_server_port = 32348
do anylog_rest_port = 32348

if !node_type == generic then
do anylog_server_port = 32548
do anylog_rest_port = 32548

if $ANYLOG_SERVER_PORT then anylog_server_port = $ANYLOG_SERVER_PORT
if $TCP_BIND == true or $TCP_BIND == True or $TCP_BIND == TRUE then tcp_bind = true

if $ANYLOG_REST_PORT then anylog_rest_port = $ANYLOG_REST_PORT
if $REST_BIND == true or $REST_BIND == True or $REST_BIND == TRUE then rest_bind = true

if $ANYLOG_BROKER_PORT then anylog_broker_port = $ANYLOG_BROKER_PORT
if $BROKER_BIND == true or $BROKER_BIND == True or $BROKER_BIND == TRUE then broker_bind = true

:sql-database:
default_dbms=!company_name.name
db_type = sqlite
set memory = false

if $DEFAULT_DBMS then default_dbms = $DEFAULT_DBMS
if !node_type == query then set memory=true

:nosql-database:
set blobs_dbms = false
set blobs_folder = true
set blobs_compress = true
set blobs_reuse = true

:blockchain:
ledger_conn = !ip + ":32048"
blockchain_sync = 30 seconds
set blockchain_source = master
set blockchain_destination = file

if $LEDGER_CONN then ledger_conn = $LEDGER_CONN

:operator-settings:
set enable_partitions = true
cluster_name = !node_name.name + -cluster
table_name=*
partition_column = insert_timestamp
partition_interval = day
partition_keep = 3
partition_sync = 1 day

:mqtt:
set enable_mqtt = false
mqtt_broker = driver.cloudmqtt.com
mqtt_port = 18785
mqtt_user = ibglowct
mqtt_passwd = MSY4e009J7ts
mqtt_topic = anylogedgex-demo
set mqtt_log = false
set mqtt_dbms = !default_dbms
mqtt_table = "bring [sourceName]"
mqtt_timestamp_column = now
mqtt_value_column_type = float
mqtt_value_column = "bring [readings][][value]"

if $ENABLE_MQTT == true or $ENABLE_MQTT == True or $ENABLE_MQTT == TRUE then set enable_mqtt = $ENABLE_MQTT

:other-settings:
set deploy_local_script = false
set create_table = true
set update_tsd_info = true
set archive = true
set distributor = true
set compress_file = true
set move_json = true
set write_immediate = true
operator_threads = 3
query_pool = 6
archive_delete=30

dbms_file_location = file_name[0]
table_file_location = file_name[1]
threshold_time = 60 seconds
threshold_volume = 10KB

if $DEPLOY_LOCAL_SCRIPT == true or $DEPLOY_LOCAL_SCRIPT == True or $DEPLOY_LOCAL_SCRIPT == TRUE then set deploy_local_script=true

:end-script:
end script

:terminate-scripts:
exit scripts

:missing-node-type:
print "Missing node type, cannot continue..."
goto terminate-scripts

:missing-node-name:
print "Missing node name, cannot continue..."
goto terminate-scripts

:missing-license-key:
print "Missing license key, cannot continue..."
goto terminate-scripts

:missing-company-name:
print "Missing company name, cannot continue..."
goto terminate-scripts

:missing-ledger-conn:
print "Missing ledger connection information, cannot continue..."
goto terminate-scripts

:invalid-sql-database:
print "Invalid SQL database type " $DB_TYPE ", cannot continue..."
goto terminate-scripts

:invalid-nosql-database:
print "Invalid NoSQL database type " $NOSQL_TYPE ", cannot continue..."
goto terminate-scripts
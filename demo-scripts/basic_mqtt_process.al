#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an MQTT client against either a publisher or operator.
# Currently the code supports both a regular MQTT client and an MQTT client against the REST node. The decision by which
#   code is deployed depends ont the parameters set by the user.
# :Required Params:
#   - MQTT Broker
#   - MQTT Port
#   - MQTT Topic -- if topic is not set, the code supports all topics against the connection
# :Optional Params set by code (if not declared):
#   - MQTT Topic -- if topic is not set, the code supports all topics against the connection
#   - MQTT Log   -- if log isn't set, th code will configure it to be false.
#   - MQTT Value Column Type -- if the column type isn't supported, then the default type is str
#       Supported Types: str, int, float, bool, timestamp
#   - Column Timestamp -- if not set, the default is `now`
# :Optional Parmas:
#   - MQTT Database
#   - MQTT Table
#   - Column Timestamp (name)
#   - Column Value (name)
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/sample_code/basic_mqtt_process.al

:set-params:
on error ignore
if $MQTT_BROKER then broker = $MQTT_BROKER
else if not !broker and !anylog_broker_port then broker = local
else if not !broker then broker = rest

if $MQTT_PORT then mqtt_port = $MQTT_PORT
else if not !mqtt_port and !anylog_broker_port then set mqtt_port = !anylog_broker_port
else if not !mqtt_port then mqtt_port = !anylog_rest_port

if $MQTT_LOG then set mqtt_log = $MQTT_LOG
if !mqtt_log != true and !mqtt_log != false then set mqtt_log = false

if $MQTT_USER then mqtt_user = $MQTT_USER
if $MQTT_PASSWD then mqtt_passwd = $MQTT_PASSWD

if $MQTT_TOPIC then mqtt_topic = $MQTT_TOPIC
else mqtt_topic = *

if $MQTT_DBMS then mqtt_dbms = $MQTT_DBMS
if $MQTT_TABLE then mqtt_table = $MQTT_TABLE
if $MQTT_TIMESTAMP_COLUMN then mqtt_timestamp_column = $MQTT_TIMESTAMP_COLUMN
if $MQTT_VALUE_COLUMN then
do mqtt_value_column = $MQTT_VALUE_COLUMN
do if $MQTT_VALUE_COLUMN_TYPE then mqtt_value_column_type = $MQTT_VALUE_COLUMN_TYPE
<do if !mqtt_value_column_type != str and
       !mqtt_value_column_type != int and
       !mqtt_value_column_type != float and
       !mqtt_value_column_type != timestamp and
       !mqtt_value_column_type != bool then mqtt_value_column_type = str
>

if !broker != rest then goto mqtt-regular

:mqtt-rest:
on error goto mqtt-error
if !mqtt_user and !mqtt_passwd and !mqtt_dbms and !mqtt_table and !mqtt_timestamp_column and !mqtt_value_column then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd and
    log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table and
        column.timestamp.timestamp=!mqtt_timestamp_column and
        column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
    )>

else if !mqtt_user and !mqtt_passwd and !mqtt_dbms and !mqtt_table then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd and 
    log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table
)>

else if !mqtt_user and !mqtt_passwd then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd
    and log=!mqtt_log and topic=(name=!mqtt_topic)>

else if !mqtt_dbms and !mqtt_table and !mqtt_timestamp_column and !mqtt_value_column then
<do run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table and
        column.timestamp.timestamp=!mqtt_timestamp_column and
        column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
)>

else if !mqtt_dbms and !mqtt_table then
<do run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table
)>
else run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(name=!mqtt_topic)

goto end-script

:mqtt-regular:
on error goto mqtt-error
if !mqtt_user and !mqtt_passwd and !mqtt_dbms and !mqtt_table and !mqtt_timestamp_column and !mqtt_value_column then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd and
    log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table and
        column.timestamp.timestamp=!mqtt_timestamp_column and
        column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
    )>

else if !mqtt_user and !mqtt_passwd and !mqtt_dbms and !mqtt_table then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd and
    log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table
)>

else if !mqtt_user and !mqtt_passwd then
<do run msg client where broker=!broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd
    and log=!mqtt_log and topic=(name=!mqtt_topic)>

else if !mqtt_dbms and !mqtt_table and !mqtt_timestamp_column and !mqtt_value_column then
<do run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table and
        column.timestamp.timestamp=!mqtt_timestamp_column and
        column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
    )>

else if !mqtt_dbms and !mqtt_table then
<do run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(
        name=!mqtt_topic and
        dbms=!mqtt_dbms and
        table=!mqtt_table
)>
else run msg client where broker=!broker and port=!mqtt_port and log=!mqtt_log and topic=(name=!mqtt_topic)


:end-script:
end script

:mqtt-error:
echo "Error: Failed to execute `run msg client` command"
goto end-script







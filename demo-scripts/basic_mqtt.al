#--------------------------------------------------------------------------------------------------------------#
# (basic) MQTT process based on configuration
#--------------------------------------------------------------------------------------------------------------#
# process $ANYLOG_PATH/demo-scripts/basic_mqtt.al

if !mqtt_broker == rest then
<do run msg client where broker=!mqtt_broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd and
user-agent=anylog and log=!mqtt_log and topic=(
    name=!mqtt_topic and
    dbms=!mqtt_dbms and
    table=!mqtt_table and
    column.timestamp.timestamp=!mqtt_timestamp_column and
    column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
)>
if !mqtt_broker != rest then
<do run msg client where broker=!mqtt_broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_passwd
and log=!mqtt_log and topic=(
    name=!mqtt_topic and
    dbms=!mqtt_dbms and
    table=!mqtt_table and
    column.timestamp.timestamp=!mqtt_timestamp_column and
    column.value=(type=!mqtt_value_column_type and value=!mqtt_value_column)
)>

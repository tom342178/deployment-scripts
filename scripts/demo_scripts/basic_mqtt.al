#--------------------------------------------------------------------------------------------------------------#
# (basic) MQTT process based on configuration
#--------------------------------------------------------------------------------------------------------------#
# process !local_scripts/demo_scripts/basic_mqtt.al

if !mqtt_broker == rest then
<do run mqtt client where broker=!mqtt_broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_paasword and
user-agent=anylog and log=!mqtt_log and topic=(
    name=!mqtt_topic and
    dbms=!mqtt_dbms and
    table=!mqtt_table and
    column.timestamp.timestamp=!mqtt_timestamp_column and
    column.value=(type=!mqtt_value_column_type aand value=!mqtt_value_column)
)>
<else run mqtt client where broker=!mqtt_broker and port=!mqtt_port and user=!mqtt_user and password=!mqtt_paasword
and log=!mqtt_log and topic=(
    name=!mqtt_topic and
    dbms=!mqtt_dbms and
    table=!mqtt_table and
    column.timestamp.timestamp=!mqtt_timestamp_column and
    column.value=(type=!mqtt_value_column_type aand value=!mqtt_value_column)
)>
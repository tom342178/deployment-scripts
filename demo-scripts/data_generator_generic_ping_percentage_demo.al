#-----------------------------------------------------------------------------------------------------------------------
# The following provides an MQTT or REST client for Ping and PerecentageCPU sensor
# :sample data:
#   {
#        "dbms": "test",
#        "table": "ping_sensor",
#        "device_name": "Catalyst 3500XL",
#        "parentelement": "68ae8bef-92e1-11e9-b465-d4856454f4ba",
#        "webid": "F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw",
#        "value": 41.7,
#        "timestamp": "2023-06-27T19:07:14.178393Z"
#    }
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/demo_scripts/data_generator_generic_ping_percentage_demo.al

:set-params:
on error ignore
if not !mqtt_log and $MQTT_LOG then set mqtt_log = $MQTT_LOG
else if not !mqtt_log then set mqtt_log = false

topic_name = ping-percentage

:mqtt-client:
on error goto mqtt-client-error
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.device_name.str="bring [device_name]" and
    column.parentelement.str="bring [parentelement]" and
    column.webid.str="bring [webid]" and
    column.value.float="bring [value]"
)>
<else run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.device_name.str="bring [device_name]" and
    column.parentelement.str="bring [parentelement]" and
    column.webid.str="bring [webid]" and
    column.value.float="bring [value]"
)>

:end-script:
end script

:mqtt-client-error:
echo "Failed to execute MQTT client request"
goto end-script

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return

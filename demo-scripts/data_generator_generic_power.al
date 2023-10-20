#-----------------------------------------------------------------------------------------------------------------------
# The following provides an MQTT or REST client for Power data
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
# process !local_scripts/demo_scripts/data_generator_generic_power.al

:set-params:
on error ignore
if not !mqtt_log and $MQTT_LOG then set mqtt_log = $MQTT_LOG
else if not !mqtt_log then set mqtt_log = false

topic_name = power-data

:mqtt-client:
on error goto mqtt-client-error
if !anylog_broker_port then
<do run mqtt client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.location=(type=str and value="bring [location]") and
    column.value=(type=float and value="bring [value]" and optional=true) and
    column.phasor=(type=str and value="bring [phasor]" and optional=true) and
    column.frequency=(type=float and value="bring [frequency]" and optional=true) and
    column.dfreq=(type=float and value="bring [dfreq]" and optional=true) and
    column.analog=(type=float and value="bring [analog]" and optional=true)
)>
<else run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.location=(type=str and value="bring [location]") and
    column.value=(type=float and value="bring [value]" and optional=true) and
    column.phasor=(type=str and value="bring [phasor]" and optional=true) and
    column.frequency=(type=float and value="bring [frequency]" and optional=true) and
    column.dfreq=(type=float and value="bring [dfreq]" and optional=true) and
    column.analog=(type=float and value="bring [analog]" and optional=true)
)>

:end-script:
end script

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return

:mqtt-client-error:
echo "Failed to execute MQTT client request"
goto end-script


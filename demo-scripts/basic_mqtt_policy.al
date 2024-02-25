#-----------------------------------------------------------------------------------------------------------------------
# Sample MQTT policy for REST / MQTT that's policy based - basaed on  basic_mqtt.al
#-----------------------------------------------------------------------------------------------------------------------
on error ignore

set create_policy = true

:preparre-policy:
policy_id = basic-mqtt
policy = blockchain get mapping where id = !policy_id
if !policy then goto mqtt-call
if create_policy == true then goto declare-policy-error

<new_polcy = {
    "mapping"; {
        "id": !policy_name,
        "dbms": !mqtt_dbms,
        "table': !mqtt_table,
        "readings": "",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now()"
            },
            "value": {
                "type": !mqtt_value_column_type,
                "value": !mqtt_value_column
            }
        }
    }
}>

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_policy = true
goto check-policy

:mqtt-call:
on error goto mqtt-error
if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign master policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member master policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare master policy on blockchain"
goto terminate-scripts

:mqtt-error:
echo "Failed to deploy MQTT process"
goto end-script

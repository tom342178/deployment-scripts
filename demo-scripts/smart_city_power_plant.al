#----------------------------------------------------------------------------------------------------------------------#
# Mapping policy for smart city (Power Plant)
#----------------------------------------------------------------------------------------------------------------------#
# process $ANYLOG_PATH/deployment-scripts/demo-scripts/smart_city_power_plant.al

:set-params:
policy_id = smart-city-pp
if not !default_dbms then default_dbms = smart_city
topic_name = power_plant

:check-policy:
is_policy = blockchain get transform where id = !policy_id
if !is_policy then goto msg-call

:prepare-policy:
<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart Ctiy PP PLC mapper",
        "dbms": !default_dbms,
        "re_match" : "^(.{2})(\\d+)_(.*)$",
        "table": "re.group(1)",
        "column": "re.group(3)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
            },
            "device_id": {
                "value": "re.group(2)",
                "type" : "string"
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

:msg-call:
on error goto msg-error
if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!topic_name and
    policy=!policy_id
)>
else if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!topic_name and
    policy=!policy_id
)>
else if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=!topic_name and
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

:msg-error:
echo "Failed to deploy MQTT process"
goto end-script
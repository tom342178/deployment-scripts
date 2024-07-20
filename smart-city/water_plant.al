#----------------------------------------------------------------------------------------------------------------------#
# Mapping policy for smart city (Power Plant)
#:Sample Data:
# {
#  "ChemicalScale1AI.PV": 65.85875,
#  "ChemicalScale2AI.PV": 2258.8225,
#  "ChemicalScale3AI.PV": 2307.668,
#  "ChemicalScale4AI.PV": 1910.988,
#  "pHAI.PV": 9.2736,
#  "CombinedChlorinatorAI.PV": -0.3836,
#  "FreeChlorinatorAI.PV": 0.4165,
#  "RawWaterMeterAI.PV": -2.16,
#  "WaterTowerLevelAI.PV": 118.45682,
#  "CombinedTurbidityAI.PV": 0.046767812,
#  "Filter1TurbidityAI.PV": 0.037775595,
#  "Filter2TurbidityAI.PV": 0.033521898,
#  "Filter3TurbidityAI.PV": 0.020530988,
#  "RawWaterMeterTotalizer.CurDay": 0.0,
#  "RawWaterMeterTotalizer.YesDay": 265673.16,
#  "CarbonFeeder.SpeedAI.PV": 0.15,
#  "Timestamp": "2024-06-30T06:02:13.385+00:00"
# }
#----------------------------------------------------------------------------------------------------------------------#
# process !root_path/deployment-scripts/smart-city/water_plant.al


on error ignore

:set-params:
policy_id = smart-city-wp
topic_name = wp-generic

:check-policy:
is_policy = blockchain get transform where id = !policy_id
if !is_policy then goto msg-call

:prepare-policy:
<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart City WP PLC mapper",
        "dbms": !default_dbms,
        "re_match" : "([^.]*)\\.(.*)",
        "table": "re.group(2)",
        "column": "re.group(1)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
            },
            "id": {
                "value": "re.group(1)",
                "type" : "float"
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
if !is_demo == true then goto end-script

on error goto msg-error
if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!topic_name and
    policy=!policy_id
)>
else if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!topic_name and
    policy=!policy_id)>
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
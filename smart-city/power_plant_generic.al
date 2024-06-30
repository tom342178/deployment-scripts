#-----------------------------------------------------------------------------------------------------------------------
# Policy to extract information for devices with ID for PowerPlant
# :Sample Data:
# {"BG10.A_Current":0,"BG10.A_N_Voltage":0,"BG10.B_Current":0,"BG10.B_N_Voltage":0,"BG10.C_Current":0,
#  "BG10.C_N_Voltage":0,"BG10.EnergyMultiplier":1,"BG10.Frequency":6000,"BG10.PowerFactor":100,"BG10.ReactivePower":0,
#  "BG10.RealPower":0,"BG11.A_Current":0,"BG11.A_N_Voltage":0,"BG11.B_Current":0,"BG11.B_N_Voltage":0,"BG11.C_Current":0,
#  ..., "Timestamp":"2024-06-30T03:27:55.8240000Z"}
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/smart-city/power_plant_generic.al

on error ignore

:prepare-policy:
policy_id = smart-city-pp
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call

:create-policy:
set new_policy = ""
<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart City PP PLC mapper",
        "dbms": !default_dbms,
        "re_match" : "^(.{2})(\\d+)\\.(.*)$",
        "table": "re.group(1)",
        "column": "re.group(3)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
            },
            "id": {
                "value": "re.group(2)",
                "type" : "string"
            }
        }

    }
}>

:test-policy:
test_policy = json !new_policy test
if !test_policy == false then goto test-policy-error

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:test-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts

:policy-error:
print "Failed to publish policy for an unknown reason"
goto terminate-scripts


:msg-error:
echo "Failed to deploy MQTT process"
goto end-script

#-----------------------------------------------------------------------------------------------------------------------
# Policy to extract information for devices without ID for PowerPlant
# :Sample Data:
#  {"BCT.A_Current":81,"BCT.A_N_Voltage":732,"BCT.B_Current":80,"BCT.B_N_Voltage":735,"BCT.C_Current":85,
#   "BCT.C_N_Voltage":733,"BCT.EnergyMultiplier":1,"BCT.Frequency":6000,"BCT.PowerFactor":96,"BCT.ReactivePower":532,
#   "BCT.RealPower":1719,"CBT.A_Current":81,"CBT.A_N_Voltage":733,"CBT.B_Current":81,"CBT.B_N_Voltage":736,
#   "CBT.C_Current":85,"CBT.C_N_Voltage":735,"CBT.EnergyMultiplier":1,"CBT.Frequency":6000,"CBT.PowerFactor":96,
#   ..., "Timestamp":"2024-06-30T05:35:58.5460000Z"}
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/smart-city/power_plant_other.al

on error ignore

# declare policy
:prepare-policy:
policy_id = smart-city-pp-others
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call

:create-policy:
set new_policy = ""
<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart City PP PLC mapper - other",
        "dbms": !default_dbms,
        "re_match" : "([^.]*)\\.(.*)",
        "table": "re.group(1)",
        "column": "re.group(2)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
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

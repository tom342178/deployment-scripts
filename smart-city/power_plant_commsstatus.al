#-----------------------------------------------------------------------------------------------------------------------
# Policy to extract Commsstatus information about PLC for PowerPlant
# :Sample Data:
# {"BG10.CommsStatus":true,"BG11.CommsStatus":true,"BG8.CommsStatus":true,"BG9.CommsStatus":true,"CG12.CommsStatus":true,
#  "CG7.CommsStatus":true,"DG2.CommsStatus":true,"DG3.CommsStatus":true,"DG4.CommsStatus":true,"DG5.CommsStatus":true,
#  "DG6.CommsStatus":true,"BCT.CommsStatus":true,"BF1.CommsStatus":true,"BF2.CommsStatus":true,"BF3.CommsStatus":true,
#  "id":914,"Timestamp":"2024-06-30T03:27:32.1940000Z"}
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/smart-city/power_plant_commsstatus.al

on error ignore

# declare policy
:prepare-policy:
policy_id = smart-city-pp-commsstatus
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call

:create-policy:
set new_policy = ""
<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart City PP PLC mapper - commsstatus",
        "dbms": !default_dbms,
        "re_match" : "([^.]*)\\.(.*)",
        "table": "commsstatus",
        "column": "re.group(1)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[Timestamp]",
                "default" : "now()"
            }
        }
    }
}>s

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

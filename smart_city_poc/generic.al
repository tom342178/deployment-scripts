#----------------------------------------------------------------------------------------------------------------------#
# Create generic policy where each component is its policy - for power plants, multiple devices would end up in the same
# table; however, for [waste] water plants, each device has unique components
# :Data from Dynics:
#   {
#       "table": recordBatch.Column(field.Name),
#       "device": field.Name,
#       recordBatch.Column(field.Name): recordBatch.Column(field.Name).GetValue(0)
#   }
#----------------------------------------------------------------------------------------------------------------------#

:set-params:
policy_id = cos-generic-policy
if not !default_dbms then default_dbms=cos

:prepare-policy:
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call

:create-policy:
set new_policy = ""
<new_policy = {
    "id": !policy_id,
    "dbms": !default_dbms,
    "table": "bring [table]",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now(),
            "bring": "[timestamp]",
        },
        "device: {
            "type": "string",
            "bring": "[device]"
        },
        "value": {
            "type": "string",
            "bring": "[recordBatch.Column(field.Name)]"
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

:msg-call:
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
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

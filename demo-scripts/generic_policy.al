#-----------------------------------------------------------------------------------------------------------------------
# Generic Policy
# :requirements:
#   -> table name
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/demo-scripts/generic_policy.al

on error ignore

:set-params:
policy_id = generic_policy
# user should specify table name
set table_name = ""
set new_policy = ""
set readings = ""
set is_epoch = false
if !is_policy then goto msg-call
if not !table_name then goto table-name-error
set create_policy = false

:check-policy:
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call
if !create_policy == true then goto declare-policy-error

:create-policy:
if !is_epoch == true then
<do new_policy={"mapping" : {
    "id" : "bc-policy",
    "company": !company_name
    "dbms" : !default_dbms,
    "table": !table_name,
    "readings": !readings,
    "schema" : {
        "timestamp" : {
            "type" : "timestamp",
            "default": "now()",
            "bring" : "[timestamp]",
            "apply" :  "epoch_to_datetime"
        },
        "*": {
            "type": "*",
            "bring": ["*"]
        }
    }
}}>
if !is_epoch == false then
<do new_policy={"mapping" : {
    "id" : "bc-policy",
    "company": !company_name
    "dbms" : !default_dbms,
    "table": !table_name,
    "readings": !readings,
    "schema" : {
        "timestamp" : {
            "type" : "timestamp",
            "default": "now()",
            "bring" : "[timestamp]"
        },
        "*": {
            "type": "*",
            "bring": ["*"]
        }
    }
}}>


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

:table-name-error:
print "Missing table name - cannot create policy"
goto end-script

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

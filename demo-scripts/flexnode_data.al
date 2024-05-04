#----------------------------------------------------------------------------------------------------------------------#
# Sample policy for Flexnode data demonstrating unknown schema information
# :sample-data:
# { "fields":{
#    "temp_crit":102, "temp_crit_alarm":0, "temp_input":47, "temp_max":92
#   },
#   "name":"lm_sensors",
#   "tags":{
#       "chip":"coretemp-isa-0001","feature":"core_0","host":"node-1"
#   },
#   "timestamp": 1713978540
# }
#----------------------------------------------------------------------------------------------------------------------#
# process $ANYLOG_PATH/deployment-scripts/demo-scripts/flexnode_data.al

on error ignore
set create_policy = false

:preparre-policy:
policy_id = telegraf-mapping
topic_name=flexnode-data
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call
if !create_policy == true  and not !policy then goto declare-policy-error

<new_policy = {"mapping" : {
        "id" : !policy_id,
        "dbms" : !default_dbms,
        "table" : "telegraf_data",
        "readings": "metrics",
        "schema" : {
                "timestamp" : {
                    "type" : "timestamp",
                    "default": "now()",
                    "bring" : "[timestamp]",
                    "apply" :  "epoch_to_datetime"
                },
                "*" : {
                    "type": "*",
                    "bring": ["fields", "tags"]
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


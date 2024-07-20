#-----------------------------------------------------------------------------------------------------------------------
# Power Plant Main
# :steps:
#   1. declare policies on blockchain
#   2 if not demo - execute run mqtt
#-----------------------------------------------------------------------------------------------------------------------
# process !root_path/deployment-scripts/smart-city/power_plant.al
on error ignore

:declare-policies:
process !root_path/deployment-scripts/smart-city/power_plant_generic.al
process !root_path/deployment-scripts/smart-city/power_plant_commsstatus.al
process !root_path/deployment-scripts/smart-city/power_plant_other.al

:msg-call:
if !is_demo == true then goto end-script

on error goto msg-error
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and
    topic=(name=pp-generic and policy=smart-city-pp) and
    topic=(name=pp-commsstatus and policy=smart-city-pp-commsstatus) and
    topic=(name=pp-other and policy=smart-city-pp-other)>


if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and
    topic=(name=pp-generic and policy=smart-city-pp) and
    topic=(name=pp-commsstatus and policy=smart-city-pp-commsstatus) and
    topic=(name=pp-other and policy=smart-city-pp-other)>

if not !anylog_broker_port and not !user_name and not !user_password then then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and
    topic=(name=pp-generic and policy=smart-city-pp) and
    topic=(name=pp-commsstatus and policy=smart-city-pp-commsstatus) and
    topic=(name=pp-other and policy=smart-city-pp-other)>

:end-script:
end script

:terminate-scripts:
exit scripts
s
:msg-error:
echo "Failed to deploy MQTT process"
goto end-script

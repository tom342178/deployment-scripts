#-----------------------------------------------------------------------------------------------------------------------
# The following allows accepting livefeed images through camera using OpenCV. The data generator example used is:
#   ~/Sample-Data-Generator/data_generator_cv2_livefeed.py
#
# :sample data coming in:
#   {
#        'dbms': 'test',
#        'table': 'video2',
#        'camera': 0,
#        'ts': '2023-03-13T23:06:51.992891Z',
#        'frame': array(
#            [[
#                [0, 0, 0],
#                [0, 0, 0],
#                [0, 0, 0],
#                ...,
#                [0, 1, 0],
#                [0, 1, 0],
#                [0, 1, 0]],
#                ...,
#            ]],
#            dtype=uint8
#        ),
#        'value': 57.93,
#        'unit': 'Celsius'
#   }
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/sample_code/livefeed_opencv.al

:create-policy:
on error ignore
policy_id = livefeed
<new_policy={"mapping": {
    "id": !policy_id,
    "dbms": "bring [dbms]",
    "table": "bring [table]",
    "timestamp": {
        "type": "timestamp",
        "bring": "[ts]"
    },
    "camera": {
        "type": "int",
        "bring": "[camera]"
    },
    "file": {
        "blob": true,
        "bring": "[frame]",
        "extension": "png",
        "apply": "opencv",
        "hash": "md5",
        "type": "varchar"
    },
    "value": {
        "type": "float",
        "bring": "[value]"
    },
    "unit": {
        "type": "string",
        "bring": "[unit]"
    }
}}>

:declare-policy:
on error call declare-policy-error
is_policy = blockchain get mapping where id = !policy_id
if not !is_policy then
do blockchain prepare policy !schedule_policy
do blockchain insert where policy=!schedule_policy and local=true and master=!ledger_conn

:mqtt-client:
on error goto mqtt-client-error
if not !mqtt_log and $MQTT_LOG then set mqtt_log = $MQTT_LOG
else if not !mqtt_log then set mqtt_log = false

if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and
    user-agent=anylog and log=!mqtt_log and topic=(
        name=!policy_id and
        policy=!policy_id
)>
else if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!policy_id and
    policy=!policy_id
)>

:end-script:
end script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return

:mqtt-client-error:
echo "Failed to start MQTT client"
goto end-script
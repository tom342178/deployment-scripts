#-----------------------------------------------------------------------------------------------------------------------
# The following is a combination of getting data from both videos and images using base64 decoding
#   -> add image policy
#   -> add video policy
#   -> run mqtt client with broker
# :process:
#   1. Start video / image process on AnyLog
#   2. Start Data generator
# :note:
#   - generic video processing: !local_scripts/sample_code/blob_video_data.al
#   - generic image processing: !local_scripts/sample_code/blob_image_data.al
# :sample-data:
# {
#        "id": "f85b2ddc-761d-88da-c524-12283fbb0f21",
#        "dbms": "ntt",
#        "table": "deeptector",
#        "file_name": "20200306202533614.jpeg",
#        "file_type": "image/jpeg",
#        "file_content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD",
#        "detection": [
#                {"class": "kizu", "bbox": [666, 275, 682, 291], "score": 0.83249},
#                {"class": "kizu", "bbox": [669, 262, 684, 277], "score": 0.83249},
#                {"class": "kizu", "bbox": [688, 261, 706,276], "score": 0.72732},
#                {"class": "kizu", "bbox": [698, 277, 713, 292], "score": 0.72659},
#        ],
#        "status": "ok"
# }
# {
#   "apiVersion": "v2",
#   "id": "6b055b44-6eae-4f5d-b2fc-f9df19bf42cf",
#   "deviceName": "anylog-data-generator",
#   "origin": 1660163909,
#   "profileName": "anylog-video-generator",
#   "readings": [{
#       "start_ts": "2022-01-01 00:00:00",
#       "end_ts": "2022-01-01 00:00:05",
#       "binaryValue": "AAAAHGZ0eXBtcDQyAAAAAWlzb21tcDQxbXA0MgADWChtb292AAAAbG12aGQAAAAA3xnEUt8ZxFMAAHUwAANvyQABAA",
#       "mediaType": "video/mp4",
#       "origin": 1660163909,
#       "profileName": "traffic_data",
#       "resourceName": "OnvifSnapshot",
#       "valueType": "Binary",
#       "num_cars": 5,
#       "speed": 65.3
#   }],
#   "sourceName": "OnvifSnapshot"
# }
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/demo_scripts/demo_video_images.al

:set-params:
image_policy_id = image-mapping
video_policy_id = video-mapping

if not !mqtt_log and $MQTT_LOG then set mqtt_log = $MQTT_LOG
else if not !mqtt_log then set mqtt_log = false


:add-image-policy:
on error ignore
is_policy = blockchain get mapping where id = !image_policy_id
if !is_policy then goto add-video-policy
if not !is_policy then
<do mapping_policy = {
    "mapping": {
    "id": !image_policy_id,
    "dbms": "bring [dbms]",
    "table": "bring [table]",
	"readings": "detection",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()"
        },
        "file": {
            "root" : true,
            "blob" : true,
            "bring" : "[file_content]",
            "extension" : "jpeg",
            "apply" : "base64decoding",
            "hash" : "md5",
            "type" : "varchar"
        },
        "class": {
            "type": "string",
            "bring": "[class]",
            "default": ""
        },
        "bbox": {
            "type": "string",
            "bring": "[bbox]",
            "default": ""
        },
        "score": {
            "type": "float",
            "bring": "[score]",
            "default": -1
        },
        "status": {
            "root": true,
            "type": "string",
            "bring": "[status]",
            "default": ""
        }
	}
    }
}>
do test_policy = json !mapping_policy test
do if !test_policy == false then goto json-policy-error

on error call declare-policy-error
if not !is_policy then 
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

:add-video-policy:
on error ignore
is_policy = blockchain get mapping where id = !video_policy_id
if !is_policy then goto mqtt-client
if not !is_policy then
<do mapping_policy = {
    "mapping": {
        "id": !video_policy_id,
        "dbms": "bring [dbName]",
        "table": "bring [deviceName]",
        "source": {
            "bring": "[deviceName]",
            "default": "car_data"
        },
        "readings": "readings",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]"
            },
            "start_ts": {
                "type": "timestamp",
                "bring": "[start_ts]"
            },
            "end_ts": {
                "type": "timestamp",
                "bring": "[end_ts]"
            },
            "file": {
                "blob": true,
                "bring": "[binaryValue]",
                "extension": "mp4",
                "apply": "base64decoding",
                "hash": "md5",
                "type": "varchar"
            },
            "file_type": {
                "bring": "[mediaType]",
                "type": "string"
            },
            "num_cars": {
                "bring": "[num_cars]",
                "type": "int"
            },
            "speed": {
                "bring": "[speed]",
                "type": "float"
            }
        }
    }
}>
do test_policy = json !mapping_policy test
do if !test_policy == false then goto json-policy-error

on error call declare-policy-error
if not !is_policy then 
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

:mqtt-client:
on error goto mqtt-client-error
if !anylog_broker port then
<do run mqtt client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!image_policy_id and
    policy=!image_policy_id
) and topic=(
    name=!video_policy_id and
    policy=!video_policy_id
)>
<else run mqtt client where broker=local and port=!anylog_rest_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!image_policy_id and
    policy=!image_policy_id
) and topic=(
    name=!video_policy_id and
    policy=!video_policy_id
)>

:end-script:
end script

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return

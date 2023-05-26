#-----------------------------------------------------------------------------------------------------------------------
# The following is a combination of getting data from both videos and images - used as part of our demo / test network
#   -> add image policy
#   -> add video policy
#   -> run mqtt client with broker
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/sample_code/demo_video_images.al

:set-params:
image_policy_id = image-mapping
video_policy_id = video-mapping

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
<run mqtt client where broker=local and port=!anylog_broker_port and log=false and topic=(
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

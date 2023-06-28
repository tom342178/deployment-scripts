#-----------------------------------------------------------------------------------------------------------------------
# The following provides an example for accepting video data into MongoDB. The example uses REST broker process, but the
# same can be applied with MQTT, and the policy is similar to what EdgeX generates. When deploying script on a publisher
# node, make sure the default logical database (!default_dbms) is set to an existing logical database.
#
# :AnyLog process:
#   0. Connect to (NoSQL) logical database
#   1. Set parameters
#   2. declare mapping policy
#   3. execute `run mqtt client`
#   4. From the outside deploy data generator
#       python3 $HOME/Sample-Data-Generator/data_generator_file_processing.py ~/Downloads/sample_data/videos/ ${REST_CONN_INFO} post \
#           --topic video-mapping \
#           --dbms test \
#           --table videos \
#           --enable-timezone-range \
#           --exception
#
# :sample data coming in:
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
#
# :documents:
#   - Generic MQTT script: !local_scripts/deployment_scripts/mqtt.al
#   - Documentation: https://github.com/AnyLog-co/documentation/blob/master/image%20mapping.md
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/demo_scripts/edgex_video_demo_base64.al

if not !mqtt_log then set mqtt_log = false
if not !default_dbms then default_dbms=test

# declare policy
:prepare-policy:
policy_id = anylogedgex-video-demo # used also as the mqtt topic name
policy = blockchain get mapping where id = !policy_id

if not !policy then
<do mapping_policy = {
    "mapping": {
        "id": !policy_id,
        "dbms": "bring [dbms]",
        "table": "bring [table]",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "default": "now()"
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
                "bring": "[file_content]",
                "extension": "mp4",
                "apply": "base64decoding",
                "hash": "md5",
                "type": "varchar"
            },
            "people_count": {
                "bring": "[count]",
                "type": "int"
            },
            "confidence": {
                "bring": "[confidence]",
                "type": "float"
            }
        }
    }
}>
do test_policy = json !mapping_policy test
do if !test_policy == false then goto json-policy-error

:declare-policy
on error call declare-policy-error
policy = blockchain get mapping where id=!policy_id
if not !policy then
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

:mqtt-call:
on error goto mqtt-error
if !anylog_broker_port then
<do run mqtt client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!policy_id and
    policy=!policy_id
)>
<else run mqtt client where broker=rest and port=!anylog_rest_port and log=!mqtt_log and topic=(
    name=!policy_id and
    policy=!policy_id
)>

:end-script:
end script

:declare-params-error:
echo "Failed to declare one or more policies. Cannot continue..."
goto end-script

:connect-dbms-error:
echo "Failed to connect to MongoDB logical database " !mongo_db_name ". Cannot continue..."
goto end-script

:blobs-archiver-error:
echo "Failed to enable blobs archiver"
return

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return


:mqtt-error:
echo "Failed to deploy MQTT process"
goto end-script



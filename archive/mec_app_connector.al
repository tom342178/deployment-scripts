#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to extend Azure's mec-app-solution-accelerator to utilize AnyLog as it's broker and storage
#-- Sample JSON --
# {"data": {
#   "Classes":[{
#       "BoundingBoxes":[
#           {
#               "x":211.0123138428,
#               "y":56.5801200867
#           },
#           {
#               "x":211.0123138428,
#               "y":208.8609313965
#           },
#           {
#               "x":259.2672119141,
#               "y":56.5801200867
#           },
#           {
#               "x":259.2672119141,
#               "y":208.8609313965
#           }
#       ],
#       "Confidence":0.7317728996,
#       "EventType":"person"
#   }],
#   "EventName":"ObjectDetection",
#   "EveryTime":1682709135647,
#   "Frame":"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgYFBgYGBwkIBgcJBwYGCAsICQoKCgoKB
#   "Information":"Test message",
#   "OriginModule":"Ai inference detection",
#   "SourceId":"video_1",
#   "UrlVideoEncoded":"1.0",
#   "time_trace":[
#       {
#           "stepEnd":1682709135650,
#           "stepName":"frameSplitter",
#           "stepStart":1682709135552
#       },
#   ]
# },
# "datacontenttype":"application/json","id":"793690ea-4297-4871-8349-2828d6674e20","pubsubname":"pubsub","source":"invoke-sender-frames","specversion":"1.0","time":"2023-04-28T19:12:16Z","topic":"newDetection","traceid":"00-00000000000000000000000000000000-0000000000000000-00","traceparent":"00-00000000000000000000000000000000-0000000000000000-00","tracestate":"","type":"com.dapr.event.sent"}
# {
#    _id: BinData(3, 'GKP6rJQsDkykH9YTCT4PDg=='),
#    Information: 'Generate alert PersonDetected detecting objects person ,stop sign',
#    Frame: '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAIBAQEBAQIBAQECAgICAgQDAgICAgUEBAMEBgUGBgY',
#    CaptureTime: ISODate('2023-04-26T22:00:20.674Z'),
#    AlertTime: ISODate('2023-04-26T22:00:21.568Z'),
#    MsExecutionTime: 942,
#    MsExecutionTimeWithCommunications: 894.3739,
#    Type: 'PersonDetected',
#    Accuracy: 66.30804443359375,
#    Source: {
#        lon: 3,
#        lat: 78,
#        Name: 'Camera 6',
#        Type: 'Camera'
#    },
#    StepTimeAsDate: [
#        {
#            StepName: 'frameSplitter',
#            StepStart: ISODate('2023-04-26T22:00:20.615Z'),
#            StepStop: ISODate('2023-04-26T22:00:20.676Z'),
#            StepDuration: '61'
#        },
#        {
#            StepName: 'ai_inferencer',
#            StepStart: ISODate('2023-04-26T22:00:20.727Z'),
#            StepStop: ISODate('2023-04-26T22:00:21.234Z'),
#            StepDuration: '558'
#        },
#        {
#            StepName: 'RulesEngine',
#            StepStart: ISODate('2023-04-26T22:00:21.263Z'),
#            StepStop: ISODate('2023-04-26T22:00:21.557Z'),
#            StepDuration: '323'
#        }
#    ],
#    MatchesClasses: [
#        {
#            EventType: 'person',
#            Confidence: 0.6630804538726807,
#            BoundingBoxes: [
#                {
#                    x: 287,
#                    y: 38
#                },
#                {
#                    x: 287,
#                    y: 163
#                },
#                {
#                    x: 320,
#                    y: 38
#                },
#                {
#                    x: 320,
#                    y: 163
#                }
#            ]
#        },
#        {
#            EventType: 'person',
#            Confidence: 0.6630804538726807,
#            BoundingBoxes: [
#                {
#                    x: 287,
#                    y: 38
#                },
#                {
#                    x: 287,
#                    y: 163
#                },
#                {
#                    x: 320,
#                    y: 38
#                },
#                {
#                    x: 320,
#                    y: 163
#                }
#            ]
#        }
#    ]
# }
#-- Sample JSON --
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/sample_code/mec_app_connector.al
on error ignore

alert_topic = newAlert
is_policy = blockchain get policy where id = !alert_topic
if not !is_policy then
<do mapping_policy = {
    "mapping": {
        "id": !alert_topic,
        "dbms": "azure",
        "table": "alerts",
        "schema": {
            "id": {
                "type": "string",
                "bring": "[id]"
            },
            "timestamp": {
                "type": "timestamp",
                "bring": "[time]"
            },
            "traceid": {
                "type": "string",
                "bring": "[traceid]"
            },
            "source": {
                "type": "string",
                "bring": "[source]"
            },
            "alert_type": {
                "type": "string",
                "bring": "[type]"
            },
            "file": {
                "root" : false,
                "blob" : true,
                "apply" : "base64decoding",
                "bring" : "[data]",
                "extension" : "jpeg",
                "hash" : "md5",
                "type" : "varchar"
            }
        }
    }
}>
do test_policy = json !alert_policy test
do if !test_policy == true then goto json-policy-error
do on error call declare-policy-error
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

on error ignore

device_policy=newDetection
is_policy = blockchain get policy where id = !alert_topic
if not !is_policy then
<do mapping_policy = {
    "mapping": {
        "id": !device_policy,
        "dbms": "azure",
        "table": "device",
        "readings": "data",
        "schema": {
            "timestamp": {
                "root" : true,
                "type": "timestamp",
                "bring": "[time]"
            },
            "source_id": {
                "root" : true,
                "type": "string",
                "bring": "[id]"
            },
            "traceparent": {
                "root" : true,
                "type": "string",
                "bring": "[traceparent]"
            },
            "source": {
                "root" : true,
                "type": "string",
                "bring": "[source]"
            },
            "source_type": {
                "root" : true,
                "type": "string",
                "bring": "[type]"
            },
            "bounding_boxes": {
                "type": "string",
                "bring": "[Classes][0][BoundingBoxes]"
            },
            "confidence": {
                "type": "float",
                "bring": "[Classes][0][Confidence]"
            },
            "event_type": {
                "type": "string",
                "bring": "[Classes][0][EventType]"
            },
            "info": {
                "type": "string",
                "bring": "[Information]"
            },
            "origin_module": {
                "type": "string",
                "bring": "[OriginModule]"
            },
            "source": {
                "type": "string",
                "bring": "[SourceId]"
            },
            "file": {
                "blob" : true,
                "apply" : "base64decoding",
                "bring" : "[Frame]",
                "extension" : "jpeg",
                "hash" : "md5",
                "type" : "varchar"
            }
        }
    }
}>
do test_policy = json !alert_policy test
do if !test_policy == true then goto json-policy-error
do on error call declare-policy-error
do blockchain prepare policy !mapping_policy
do blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

on error goto mqtt-error
broker=driver.cloudmqtt.com
port=18742
user=hqpyyshb
password=bB38GEf93cPG
<run msg client where broker=!broker and port=!port and user=!user and password=!password and log=false and topic=(
    name=!alert_topic and policy=!alert_topic
) and topic=(
    name=!device_policy and policy=!device_policy
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

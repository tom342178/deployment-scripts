#-----------------------------------------------------------------------------------------------------------------------
# {
#   "SubstationID":13,
#   "Substation":"Magnolia Avenue Substation",
#   "EventDate":"2018-03-16 21:16:06",
#   "EventTypeId":15,
#   "EventDescription": "System: Control system update in progress."
# }
#-----------------------------------------------------------------------------------------------------------------------

“SubstationID”:5,
“Substation”:“Birch Street Substation”,
“EventDate”:“2021-10-11 21:16:06”,
“EventTypeId”:11,
“EventDescription”: “Security: Unauthorized access detected.“
}




<mapping_policy = {
    "mapping": {
        "id": "fusion-1",
        "dbms": !default_dbms,
        "table": "substation_events",
        "readings": "",
        "schema": {
            "timestamp" : {
                "bring": "[EventDate]",
                "default" : "now()",
                "type" : "timestamp",
                "apply" :  "epoch_to_datetime"
            },
            "substation_id": {
                "bring": "[SubstationID]",
                "type": "int"
            },
            "event_type_Id": {
                "bring": "[EventTypeId]",
                "type": "int"
            },
            "substation": {
                "bring": "[Substation]",
                "type": "str"
            },
            "system": {
                "bring": "[System]",
                "type": "str"
            },
            "event_description": {
                "bring": "[EventDescription]",
                "default": "",
                "type": "str"
            }
        }
    }
}>

blockchain prepare policy !mapping_policy
blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=fusion-1 and
    policy=fusion-1
)>


<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=fusion-1 and
    dbms=!default_dbms and
    table=substation_events and
    column.timestamp.timestamp="bring [EventDate]" and
    column.substation_id=(type=int and value="bring [SubstationID]") and
    column.event_type_Id=(type=int and value="bring [EventTypeId]") and
    column.substation=(type=str and value="bring [Substation]") and
    column.event_description=(type=str and value="bring [EventDescription]")
)>
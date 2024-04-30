policy_id = telegraf_mapping
topic = flexnode-data
anylog_broker_port = 7850

<run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!topic and
    policy=!policy_id
)>

policy_id = telegraf_mapping
<mapping_policy = {"mapping" : {

        "id" : !policy_id,

        "dbms" : "flexnode",
        "table" : "bring [name] _ [tags][name]:[tags][host]",
        "schema" : {
                "timestamp" : {
                    "type" : "timestamp",
                    "default": "now()",
                    "bring" : "[timestamp]"
                },

                "*" : {
                    "type": "*",
                    "bring": ["fields", "tags"]
                }
         }
   }
}>
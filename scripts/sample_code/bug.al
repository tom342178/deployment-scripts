policy_id = anylogedgex
set db_name = test

<mapping_policy = {"mapping" : {
    "id": !policy_id ,
    "dbms" : !db_name,
    "table" : "bring [readings][0][name]",
    "readings" : "readings",
    "schema" : {
        "timestamp" : {
            "bring": "[origin]",
            "default" : "now()",
            "type" : "timestamp",
            "apply" :  "epoch_to_datetime"
        },
        "value" : [
            {
                "table": "randomvalue_int8",
                "type": "int",
                "value": "bring [value]"
            },
            {
                "table": "randomvalue_int16",
                "type": "int",
                "value": "bring [value]"
            },
            {
                "table": "randomvalue_int32",
                "type": "int",
                "value": "bring [value]"
            },
            {
                "table": "randomvalue_int64",
                "type": "int",
                "value": "bring [value]"
            },
            {
                "bring" : "[value]",
                "type" : "float"
            }
        ]
    }
}}>

blockchain prepare policy !mapping_policy
blockchain insert where policy=!mapping_policy and local=true and master=!ledger_conn

<run mqtt client where
   broker=driver.cloudmqtt.com and
   port=18785 and
   user=ibglowct and
   password=MSY4e009J7ts and
   log=false and
   topic=(
     name=!policy_id and
    policy=!policy_id
)>
run mqtt client where broker=

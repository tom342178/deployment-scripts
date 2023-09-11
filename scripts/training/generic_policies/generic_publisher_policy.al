#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic publisher node policy
#   -> connect to TCP and REST (both not binded)
#   -> run blockchain sync
#   -> create almgm + tsd_info
#   -> prepare for deployment
#   -> execute `run publisher`
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/generic_policies/generic_publisher_policy.al
on error ignore

:is-policy:
is_policy = blockchain get config where id = generic-publisher-policy
if !is_policy then goto end-script

:declare-policy:
<new_policy = {
    "config": {
        "id": "generic-publisher-policy",
        "node_type": "publisher",
        "ip": '!external_ip',
        "local_ip": '!ip',
        "port": '!anylog_server_port.int',
        "rest_port": '!anylog_rest_port.int',
        "script": [
            "set node name !node_name",
            "run scheduler 1",
            "run blockchain sync where source=master and time=30 seconds and dest=file and connection=!ledger_conn",
            "connect dbms almgm where type=sqlite",
            "create table tsd_info where dbms=sqlite",
            "set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true",
            "run streamer",
            "run publisher where compress_json=true and compress_sql=true and master_node=!ledger_conn and dbms_name=0 and table_name=1"
        ]
}}>

process !local_scripts/training/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
echo "Failed to sign (generic) publisher policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare (generic) publisher policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to declare (generic) publisher on blockchain"
goto terminate-scripts
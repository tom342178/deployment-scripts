#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic query node policy
#   -> connect to TCP and REST (both not binded)
#   -> run blockchain sync
#   -> create system_query database in memory
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/generic_scripts/generic_query_policy.al
on error ignore

:is-policy:
is_policy = blockchain get config where id = generic-query-policy
if !is_policy then goto end-script

:declare-policy:
<new_policy = {
    "config": {
        "id": "generic-query-policy",
        "node_type": "query",
        "ip": '!external_ip',
        "local_ip": '!ip',
        "port": '!anylog_server_port.int',
        "rest_port": !anylog_rest_port,
        "scripts": [
            'set node name !node_name',
            "run scheduler 1",
            'run blockchain sync where source=master and time=30 seconds and dest=file and connection=!ledger_conn',
            "connect dbms system_query where dbms=sqlite and memory=true"
        ]
}}>

process !local_scripts/generic_scripts/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
echo "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to declare cluster policy on blockchain"
goto terminate-scripts
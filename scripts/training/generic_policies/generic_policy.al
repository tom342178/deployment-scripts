#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic node policy
#   -> connect to TCP, REST and broker (all not bind)
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/generic_policies/generic_policy.al
on error ignore

:is-policy:
is_policy = blockchain get config where id = generic-policy
if !is_policy then goto end-script

:declare-policy:
<new_policy = {
    "config": {
        "id": "generic-policy",
        "node_type": "generic",
        "ip": '!external_ip',
        "local_ip": '!ip',
        "port": '!anylog_server_port.int',
        "rest_port": '!anylog_rest_port.int',
        "broker_port": '!anylog_broker_port.int',
        "script": [
            "if not !node_name then node_node=anylog-node",
            "set node name !node_name",
            "run scheduler 1"
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
echo "Failed to sign generic  policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare generic policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to generic policy on blockchain"
goto terminate-scripts
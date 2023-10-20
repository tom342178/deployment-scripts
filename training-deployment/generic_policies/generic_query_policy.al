#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic query node policy
#   -> connect to TCP and REST (both not binded)
#   -> run blockchain sync
#   -> create system_query database in memory
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/generic_query_policy.al
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
        "rest_port": '!anylog_rest_port.int',
        "script": [
            "set node name !node_name",
            "run scheduler 1",
            "is_policy = blockchain get query where company=!company_name and name=!node_name and ip=!external_ip and port=!anylog_server_port",
            "if not !is_policy then new_policy = create policy query with defaults where name=!node_name and port=!anylog_server_port.int and rest_port=!anylog_rest_port.int and company=!company_name",
            "if not !is_policy then process !local_scripts/generic_policies/publish_policy.al",
            "run blockchain sync where source=master and time=30 seconds and dest=file and connection=!ledger_conn",
            "monitoring_nodes = blockchain get (operator,query,master) bring.ip_port",
            "set monitored nodes where topic = operator and nodes = !monitoring_nodes",
            "connect dbms system_query where type=sqlite and memory=true",
            "config from policy where id = generic-schedule-policy"
        ]
}}>

process !local_scripts/generic_policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign generic query policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare sign policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare generic query policy on blockchain"
goto terminate-scripts
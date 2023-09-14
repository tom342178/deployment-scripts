#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic master node policy
#   -> connect to TCP and REST (both not binded)
#   -> run blockchain sync
#   -> create blockchain database
#   -> create ledger table
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/generic_policies/generic_master_policy.al
on error ignore

:is-policy:
is_policy = blockchain get config where id = generic-master-policy
if !is_policy then goto end-script

:declare-policy:
<new_policy = {
    "config": {
        "id": "generic-master-policy",
        "node_type": 'master',
        "ip": '!external_ip',
        "local_ip": '!ip',
        "port": '!anylog_server_port.int',
        "rest_port": '!anylog_rest_port.int',
        "script": [
            "set node name !node_name",
            "is_policy = blockchain get master where name=!node_name and company=!company_name",
            "if not !is_policy then new_policy = create policy master with defaults where name=!node_name and port=!anylog_server_port and rest_port=!anylog_rest_port and company=!company_name and license=!license_key"
            "if not !is_policy then process !local_scripts/training/publish_policy.al",
            "run scheduler 1",
            "connect dbms blockchain where type=sqlite",
            "create table ledger where dbms=blockchain",
            "run blockchain sync where source=master and time=30 seconds and dest=file and connection=!ledger_conn",
            "config from policy where id = generic-schedule-policy"
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
echo 'Failed to sign (generic) master policy'
goto terminate-scripts

:prepare-policy-error:
echo 'Failed to prepare (generic) master policy for publishing on blockchain'
goto terminate-scripts

:declare-policy-error:
echo 'Failed to declare (generic) master policy on blockchain'
goto terminate-scripts


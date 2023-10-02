on error ignore
schedule_id = generic-schedule-policy
set create_policy = false

:check-policy:
is_policy = blockchain get schedule where id=!schedule_id

# just created the policy + exists
if !is_policy then goto config-policy

# failure show created policy
if not !is_policy and !create_policy == true then goto declare-policy-error

:schedule-policy:
new_policy=""
<new_policy = {
    "schedule": {
        "id": !schedule_id,
        "name": "Generic Monitoring Schedule",
        "script": [
	        "operator_status = test process operator",
            "if !operator_status == true then schedule name = get_operator_stat and time = 30 seconds task node_insight = get operator stat format = json",
            "if !operator_status == false then schedule name=get_node_name and time = 30 seconds task node_insight[Node name] = get node name",
            "schedule name = disk_space and time = 30 seconds task node_insight[Free space %] = get disk percentage .",
            "schedule name = cpu_percent and time = 30 seconds task node_insight[CPU %] = get node info cpu_percent",
            "schedule name = packets_recv and time = 30 seconds task node_insight[Packets Recv] = get node info net_io_counters packets_recv",
            "schedule name = packets_sent and time = 30 seconds task node_insight[Packets Sent] = get node info net_io_counters packets_sent",
            "schedule name = errin and time = 30 seconds task errin = get node info net_io_counters errin",
            "schedule name = errout and time = 30 seconds task errout = get node info net_io_counters errout",
            "schedule name = error_count and time = 30 seconds task node_insight[Network Error] = python int(!errin) + int(!errout)",
            "schedule name = monitor_node and time = 30 seconds task run client (blockchain get !monitor_node  where company=!monitor_node_company bring.ip_port) monitor operators where info = !node_insight"
        ]
}}>

:publish-policy:
process !local_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error
set create_policy = true
goto check-policy

:config-policy:
on error goto config-policy-error
if !monitor_nodes == true then config from policy where id=!schedule_id

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign schedule policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member schedule policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare schedule policy on blockchain"
goto terminate-scripts


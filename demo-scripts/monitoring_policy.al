# process !anylog_path/deployment-scripts/demo-scripts/monitoring_policy.al
on error ignore
schedule_id = generic-schedule-policy
set create_policy = false

:store-monitoring:
if !default_dbms == monitoring or !store_monitoring == false then goto set-partitons

on error goto store-monitoring-error
if !store_monitoring == true and !db_type == psql then
<do connect dbms monitoring where
    type=!db_type and
    user = !db_user and
    password = !db_passwd and
    ip = !db_ip and
    port = !db_port and
    autocommit = !autocommit and
    unlog = !unlog>
else if !store_monitoring == true then create database monitoring where type=sqlite

:set-partitons:
if !store_monitoring == true then
do partition monitoring * using timestamp by 12 hours
do schedule time=1 day and name="Drop Monitoring" task drop partition where dbms=monitoring and table =* and keep=3

:get-operator-ip:
on error ignore
operator_monitoring_ip = blockchain get operator where name = syslog-operator1 bring.ip_port
if !node_type == operator than  operator_monitoring_ip = blockchain get operator where name = !node_name bring.ip_port
if not !operator_monitoring_ip then operator_monitoring_ip = blockchain get operator bring.first [*][ip] : [*][port]

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
            "schedule name = monitoring_ips and time=300 seconds and task monitoring_ips = blockchain get query bring.ip_port"
            "if !store_monitoring == true and !node_type != operator then schedule name = operator_monitoring_ips and time=300 seconds and task if not !operator_monitoring_ip then operator_monitoring_ip = blockchain get operator bring.first [*][ip] : [*][port]",

            "schedule name = get_stats and time=30 seconds and task node_insight = get stats where service = operator and topic = summary  and format = json",
            "schedule name = get_timestamp and time=30 seconds and task node_insight[timestamp] = get datetime local now()",
            "schedule name = get_disk_space and time=30 seconds and task value = get disk percentage ."
            "schedule name = disk_space and time = 30 seconds task node_insight[Free space %] = get disk percentage .",
            "schedule name = cpu_percent and time = 30 seconds task node_insight[CPU %] = get node info cpu_percent",
            "schedule name = packets_recv and time = 30 seconds task node_insight[Packets Recv] = get node info net_io_counters packets_recv",
            "schedule name = packets_sent and time = 30 seconds task node_insight[Packets Sent] = get node info net_io_counters packets_sent",
            "schedule name = errin and time = 30 seconds task errin = get node info net_io_counters errin",
            "schedule name = errout and time = 30 seconds task errout = get node info net_io_counters errout",
            "schedule name = error_count and time = 30 seconds task node_insight[Network Error] = python int(!errin) + int(!errout)",
            "schedule name = local_monitor_node and time = 30 seconds task monitor operators where info = !node_insight",

            "schedule name = monitor_node and time = 30 seconds task if !monitoring_ips then if !monitoring_ips then run client (!monitoring_ips) monitor operators where info = !node_insight"
            "if !store_monitoring == true and !node_type == operator then schedule name = monitor_node and time = 30 seconds task if !operator_monitoring_ip then stream !node_insight  where dbms=monitoring and table=node_insight",
            "if !store_monitoring == true and !node_type != operator then schedule name = monitor_node and time = 30 seconds task if !operator_monitoring_ip then run client (!operator_monitoring_ip) stream !node_insight  where dbms=monitoring and table=node_insight"
        ]
}}>

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_policy = true
goto check-policy

:config-policy:
on error goto config-policy-error
config from policy where id=!schedule_id

:end-script:
end script

:terminate-scripts:
exit scripts

:store-monitoring-error:
print "Faileed to store "
:config-policy-error:
print "Failed to configure node based on Schedule ID"
goto terminate-scripts

:sign-policy-error:
print "Failed to sign schedule policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member schedule policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare schedule policy on blockchain"
goto terminate-scripts


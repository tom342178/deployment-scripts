#-----------------------------------------------------------------------------------------------------------------------
# Node monitoring to be stored in variables & run through a scheduler every N seconds
#   -> if operator node then operator stats
#   -> disk space
#   -> CPU percent
#   -> Node Status
#   -> Network I/O
#
# The results for scheduled processes are sent to the different operators query nodes. The data can be viewed through
# Remote-CLI
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/monitoring/monitoring_node_policy.al
on error ignore

:set-params:
set new_policy = "" 
policy_name = Node Monitoring
monitoring_type = generic
schedule_time = 15 seconds

if !deploy_operator == true then
do policy_name = Operator Node Monitoring
do monitoring_type = operator
else if !deploy_publisher == true then then monitoring_type = publisher

policy_id_status = 0
:get-policy-id:
policy_id = blockchain get schedule where name=!policy_name and company = !company_name and monitoring_type = !monitoring_type bring [schedule][id]
if !policy_id then goto run-policy
if not !policy_id and !policy_id_status == 1 then goto  declare-policy-error

:prepare-policy:
set new_policy[schedule] = {}
set new_policy[schedule][name] = !policy_name
set new_policy[schedule][company] = !company_name
set new_policy[schedule][monitoring_type] = !monitoring_type

if !monitoring_type == operator then goto operator-monitoring

<set new_policy[schedule][script] = [
    'schedule name = get_node_stat and time = !schedule_time task node_insight = get status include statistics where format=json',
    'schedule name = disk_space and time = !schedule_time task node_insight[Free space %] = get disk percentage .',
    'schedule name = cpu_percent and time = !schedule_time task node_insight[CPU %] = get node info cpu_percent',
    'schedule name = packets_recv and time = !schedule_time task node_insight[Packets Recv] = get node info net_io_counters packets_recv',
    'schedule name = packets_sent and time = !schedule_time task node_insight[Packets Sent] = get node info net_io_counters packets_sent',
    'schedule name = errin and time = !schedule_time task errin = get node info net_io_counters errin',
    'schedule name = errout and time = !schedule_time task errout = get node info net_io_counters errout',
    'schedule name = error_count and time = !schedule_time task node_insight[Network Error] = python int(!errin) + int(!errout)',
    'schedule name = monitor_node and time = !schedule_time task run client (blockchain get !monitor_node where company=!monitor_node_company bring.ip_port) monitor operators where info = !node_insight'
]>

goto publish-policy

:operator-monitoring:
# set scripts for operator
if !deploy_operator == true then
<do set new_policy[schedule][script] = [
    'schedule name = get_operator_stat and time = !schedule_time task node_insight = get operator stat format = json',
    'schedule name = disk_space and time = !schedule_time task node_insight[Free space %] = get disk percentage .',
    'schedule name = cpu_percent and time = !schedule_time task node_insight[CPU %] = get node info cpu_percent',
    'schedule name = packets_recv and time = !schedule_time task node_insight[Packets Recv] = get node info net_io_counters packets_recv',
    'schedule name = packets_sent and time = !schedule_time task node_insight[Packets Sent] = get node info net_io_counters packets_sent',
    'schedule name = errin and time = !schedule_time task errin = get node info net_io_counters errin',
    'schedule name = errout and time = !schedule_time task errout = get node info net_io_counters errout',
    'schedule name = error_count and time = !schedule_time task node_insight[Network Error] = python int(!errin) + int(!errout)',
    'schedule name = monitor_node and time = !schedule_time task run client (blockchain get !monitor_node where company=!monitor_node_company bring.ip_port) monitor operators where info = !node_insight'
]>

:publish-policy:
process !local_scripts/deployment_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error
policy_id_status = 1

:run-policy:
on error goto config-policy-error
config from policy where id = !policy_id

:end-script:
end script

:sign-policy-error:
echo "Failed to sign assignment policy"
goto terminate-scripts

:prepare-policy-error:
echo "Failed to prepare member assignment policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
echo "Failed to declare assignment policy on blockchain"
goto terminate-scripts

:config-policy-error:
echo "Failed to configure node base on policy ID: " !policy_id
goto terminate-scripts

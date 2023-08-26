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
policy_name = Node Monitoring
if !deploy_operator == true then
do policy_id = operator-node-monitoring
do policy_name = Operator Node Monitoring
schedule_time = 15 seconds
monitoring_type = generic
if !deploy_operator == true then monitoring_type = operator
if !deploy_publisher == true then monitoring_type = publisher

:get-policy-id:
policy_id = blockchain get schedule where name=!policy_name and company = !company_name and monitoring_type = !monitoring_type bring [schedule][id]
if !policy_id then goto run-policy

:prepare-policy:
schedule_policy[schedule] = {}
schedule_policy[schedule][name] = !policy_name
schedule_policy[schedule][company] = !company_name
schedule_policy[schedule][monitoring_type] = !monitoring_type

if !monitoring_type == operator then goto operator-monitoring

<schedule_policy[schedule][script] = [
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

goto declare-node

:operator-monitoring:
# set scripts for operator
if !deploy_operator == true then
<do schedule_policy[schedule][script] = [
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

:declare-node:
on error call declare-policy-error
if not !is_policy then
do blockchain prepare policy !schedule_policy
do blockchain insert where policy=!schedule_policy and local=true and master=!ledger_conn
goto get-policy-id

:run-policy:
on error goto run-policy-error
config from policy where id = !policy_id

:end-script:
end script

:declare-policy-error:
echo "Error: Failed to declare resource policy."
goto run-policy

:run-policy-error:
echo "Error: failed to run process from policy"
goto end-script


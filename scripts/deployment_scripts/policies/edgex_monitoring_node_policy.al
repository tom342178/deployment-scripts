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
# process !local_scripts/deployment_scripts/policies/monitoring_node_policy.al
on error ignore

:set-params:
policy_id = edgex-monitoring
policy_name = EdgeX Monitoring
schedule_time = 15 seconds
edgex_delete_url = "http://" + !external_ip + ":59880/api/v2/event/age/86400000000000"

is_policy = blockchain get schedule where id = !policy_id and company = !company_name
if !is_policy then goto run-policy

:prepare-policy:
schedule_policy[schedule] = {}
schedule_policy[schedule][id] = !policy_id
schedule_policy[schedule][name] = !policy_name
schedule_policy[schedule][company] = !company_name
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
    'schedule name = clean_edgex and time = 1 day task rest delete url = !edgex_delete_url'
]>

# set scripts for operator
if !deploy_ledger == false or !deploy_operator == true or !deploy_publisher == true or !deploy_query == true then
<do schedule_policy[schedule][script] = [
    'schedule name = clean_edgex and time = 1 day task rest delete url = !edgex_delete_url'
]>

on error call declare-policy-error
if not !is_policy then
do blockchain prepare policy !schedule_policy
do blockchain insert where policy=!schedule_policy and local=true and master=!ledger_conn

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


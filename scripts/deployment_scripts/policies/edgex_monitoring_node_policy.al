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
# process !local_scripts/deployment_scripts/policies/edgex_monitoring_node_policy.al
on error ignore

:set-params:
policy_id = edgex-purge
policy_name = Edgex Purge
schedule_time = 1 day
edgex_delete_url = "http://" + !external_ip + ":59880/api/v2/event/age/"

:calculate-age:
hours=24
seconds  = python int(!hours) * 3600
nanoseconds = python int(!seconds) * 1000000000
edgex_delete_url = !edgex_delete_url + !nanoseconds

:check-policy:
is_policy = blockchain get schedule where id = !policy_id and name=!policy_name and company=!company_name
if !is_policy then goto run-policy

:prepare-policy:
schedule_policy[schedule] = {}
schedule_policy[schedule][id] = !policy_id
schedule_policy[schedule][name] = !policy_name
schedule_policy[schedule][company] = !company_name
schedule_policy[schedule][scripts] = [
    'schedule name = purge_edgex and time = 1 day task rest delete where url = !edgex_delete_url'
]

:declare-policy:
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


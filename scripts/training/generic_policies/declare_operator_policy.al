#----------------------------------------------------------------------------------------------------------------------#
# Declare cluster and operator policies on the blockchain
#   --> declare `operator_conn` used as host value for cluster
#   --> check cluster ID
#   --> if cluster ID DNE, create cluster policy and recheck for ID
#   --> check operator ID
#   --> if operator ID DNE, create operator policy and recheck for ID
#
# :sample-policies:
#   {'cluster' : {'company' : 'New Company',
#               'host' : '178.79.143.174:32248',
#               'name' : 'AnyLog-cluster-2',
#               'status' : 'active',
#               'id' : '1ccd858777bcc2d748c7672e848d6338',
#               'date' : '2023-09-12T22:40:39.396249Z',
#               'ledger' : 'global'
#   }},
#   {'operator' : {'company' : 'New Company',
#                'cluster' : '1ccd858777bcc2d748c7672e848d6338',
#                'name' : 'AnyLog-operator-1',
#                'ip' : '178.79.143.174',
#                'internal_ip' : '178.79.143.174',
#                'port' : 32148,
#                'rest_port' : 32149,
#                'member' : 101,
#                'id' : '9e7eaa4e0d5af9bb25dc12855d04c782',
#                'date' : '2023-09-12T22:43:23.627572Z',
#                'ledger' : 'global'
#   }}
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/training/generic_policies/declare_operator_policy.al
on error ignore
:set-params:
cluster_name = !node_name + -cluster
operator_conn = !ip + : + !anylog_server_port


:cluster-id:
cluster_id = blockchain get cluster where company=!company_name and name=!cluster_name and host=!operator_conn  bring [*][id]
if !cluster_id then goto operator-id
if not !cluster_id and !cluster_status == true then goto cluster-id-error

:prepare-cluster:
<new_policy = create policy cluster with defaults where
    company=!company_name and
    name=!cluster_name and
    host=!operator_conn>
process !local_scripts/training/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

cluster_status = true
goto cluster-id

:operator-id:
operator_id = blockchain get operator where company=!company_name and name=!node_name and cluster=!cluster_id bring [*][id]
if !operator_id then goto end-script
if not !operator_id and !operator_status == true then goto operator-id-error

:prepare-operator:
<new_policy = create policy operator with defaults where
    company=!company_name and
    name=!node_name and
    cluster=!cluster_id and
    port=!anylog_server_port and
    rest=!anylog_rest_port and
    broker=!anylog_broker_port>
process !local_scripts/training/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

operator_status == true

:end-script:
end script

:terminate-scripts:
exit scripts

:cluster-id-error:
echo "Failed to declare cluster policy, cannot continue..."
goto terminate-scripts

:operator-id-error:
echo "Failed to declare operator policy, cannot continue..."
goto terminate-scripts

:sign-policy-error:
if !j then echo "Failed to sign operator policy"
else echo "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
if !j then echo "Failed to prepare operator policy for publishing on blockchain"
else echo "Failed to prepare cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
if !j then echo "Failed to declare operator policy on blockchain"
else echo "Failed to declare cluster policy on blockchain"
goto terminate-scripts
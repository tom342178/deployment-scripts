#----------------------------------------------------------------------------------------------------------------------#
# The ANMP policy is used for updating information for a given policy. Examples include:
#   - updating an IP
#   - updating a Port
#   - changing policy name
#   - changing policy owner (company name)
#   - adding new information
#
# In this example, we're going to replace the external IP with the internal (local) IP and add a broker port (assuming
#   it exists) for a local node.
#
# (internal) URL: https://anylog.atlassian.net/wiki/spaces/ND/pages/1693220865/ANMP
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/sample_code/anmp_update_policy.al

:get-policy-id:
on error goto get-policy-id-error
if $POLICY_TYPE == ledger then node_type = master
else if $POLICY_TYPE == operator then node_type = operator
else if $POLICY_TYPE == publisher then node_type = publisher
else if $POLICY_TYPE == query then node_type = query

policy_id = blockchain get !node_type where name=!node_name and company=!company_name and ip=!external_ip and local_ip=!ip bring [*][id]
if not policy_id then goto get-policy-id-error


:update-policy:
on error ignore
if !anylog_broker_port then
<anmp_policy = {
    "anmp": {
        !policy_id: {
            "ip": !ip,
            "broker_port": 32050
        }
}}>

:sign-policy:
if !enable_auth == true then
do on error goto sign-policy-error
do id sign !anmp_policy where key = !private_key and password = !node_password

:validate-policy:
on error goto validate-policy-error
test_policy = json !anmp_policy
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call declare-policy-error
blockchain prepare policy !anmp_policy
blockchain insert where policy=!anmp_policy and local=true and master=!ledger_conn

:end-script:
end script

:get-policy-id-error:
echo "Error: Failed to policy ID to update with the given information. Cannot continue"
goto end-script

:sign-policy-error:
echo "Error: Failed to sign root member policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with root member policy declaration"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for " !policy_type
return


#-------------------------------------------------------------------------------------------------
# Associate between a node and a set of permissions. This step needs to be done with root credentials
#-------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/assignment_node.al

:set-params:
on error ignore
# this value needs to change when adding a node that is not root
policy_node_name = !node_name

permission_name = "no restrictions"

is_policy = blockchain get assignment where name=!node_name and company=!company_name and name = !permission_name
if !is_policy then goto end-script

:get-ids:
<member_certificate = blockchain get member where
    type = node and
    name = !node_name and
    company = !company_name
bring [member][public_key]>

if not !member_certificate then goto certificate-error

<permission_id = blockchain get permissions where
    name = !permission_name and
    company = !company_name
bring [permissions][id]>

if not !permission_id then goto permission-id-error

:create-policy:
<new_policy = {"assignment" : {
    "name" : !node_name,
    "company": !company_name,
    "permissions"  : !permission_id,
    "members"  : [!member_certificate]
}}>

:prepare-policy:
on error goto prepare-policy-error
new_policy = id sign !new_policy where key = !root_private_key and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:private-key-error:
echo "Failed to get private key rom generated root key"
goto end-script

:certificate-error:
echo "Failed to get public key for node policy"
goto end-script

:permission-id-error:
echo "Failed locate permission ID to associate the node against"
goto end-script

:public-key-error:
echo "Missing public key, cannot create valid member policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member root policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for root member"
return

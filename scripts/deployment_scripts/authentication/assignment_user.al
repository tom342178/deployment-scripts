#-------------------------------------------------------------------------------------------------
# Associate between a user and a set of permissions. This step needs to be done with root credentials
#-------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/assignment_user.al

:get-ids:
<member_certificate = blockchain get member where
    type = !user_type and
    name = !user_name and
    company = !company_name
bring [member][public_key]>

if not !member_certificate then goto certificate-error

<permission_id = blockchain get permissions where
    name = "limited restrictions" and
    company = !company_name
bring [permissions][id]>

if not !permission-id then goto permission-id-error

:declare-policy:
<new_policy = {"assignment" : {
    "name" : !user_name,
    "permissions"  : !permission_id,
    "members"  : [!member_certificate]
}}>

:prepare-policy:
on error goto prepare-policy-error
new_policy = id sign !new_policy where key = !new_policy and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

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
returns

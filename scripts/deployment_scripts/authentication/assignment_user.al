#-------------------------------------------------------------------------------------------------
# Associate between a user and a set of permissions. This step needs to be done with root credentials
#-------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/assignment_user.al

:set-params:
on error ignore
policy_name = !company_name + " root policy"

# these values need to change when adding a user that's not in root
policy_user_type = !user_type
policy_user_name = !user_name

is_policy = blockchain get assignment where type=!policy_user_type and name=!policy_user_name and company=!company_name
if !is_policy then goto end-script

:get-ids:
<member_certificate = blockchain get member where
    type = !policy_user_type and
    name = !policy_user_name and
    company = !company_name
bring [member][public_key]>

if not !member_certificate then goto certificate-error

<permission_id = blockchain get permissions where
    name = "limited restrictions" and
    company = !company_name
bring [permissions][id]>

if not !permission-id then goto permission-id-error

:create-policy:
<new_policy = {"assignment" : {
    "name" : !policy_user_name,
    "permissions"  : !permission_id,
    "members"  : [!member_certificate]
}}>

:publish-policy:
process !local_scripts/deployment_scripts/authentication/publish_policy_root.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:certificate-error:
echo "Failed to get public key for user policy"
goto end-script

:permission-id-error:
echo "Failed locate permission ID to associate the user against"
goto end-script

:private-key-error:
echo "Failed to get private key from generated root key"
goto end-script

:sign-policy-error:
echo "Failed to sign assignment policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member assignment policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Failed to declare assignment policy on blockchain"
goto end-script

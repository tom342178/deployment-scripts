#--------------------------------------------------------------------------------------------------------
# Create root member policy. An AnyLog network should only have 1 root member, which is used for granting
# permissions to other users and/or nodes.
#--------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/member_root_user.al

:set-params:
root_policy_name = !company_name + " root policy"

:check-policy:
is_policy = blockchain get member where type=root and company=!company_name and name=!root_policy_name
if !is_policy then goto end-script

:clean-keys:
system rm -rf !id_dir/root_keys.pem

:create-keys:
on error goto create-keys-error
id create keys where password = !root_password and keys_file = root_keys

:create-policy:
on error ignore
<new_policy = {"member": {
    "type": "root",
    "name": !root_policy_name,
    "company": !company_name
}}>

:publish-policy:
process !local_scripts/deployment_scripts/authentication/publish_policy_root.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:create-keys-error:
echo "Failed to create root keys. Cannot continue with process"
goto end-script

:sign-policy-error:
echo "Failed to sign root policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member root policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Failed to declare root policy on blockchain"
goto end-script

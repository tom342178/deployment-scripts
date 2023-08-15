#--------------------------------------------------------------------------------------------------------
# Create member policy for a node. Each node should have its own member policy.
#--------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/member_node.al

:set-params:
on error ignore
key_name = python !node_name.replace("-", "_").replace(" ", "_").strip()

:check-policy:
is_policy = blockchain get member where type=node and name=!node_name and company=!company_name
if !is_policy then goto end-script

:clean-keys:
del_name = !id_dir + !key_name + "*"
system rm -rf !del_name

:create-keys:
on error goto create-keys-error
id create keys where password = !node_password and keys_file = !key_name

:create-policy:
<new_policy = {"member": {
    "type" : "node",
    "name": !node_name,
    "company": !company_name
}}>

:publish-policy:
process !local_scripts/deployment_scripts/policies/publish_policy.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:create-keys-error:
echo "Failed to create node keys. Cannot continue with process"
goto end-script

:sign-policy-error:
echo "Failed to sign node policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member node policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Failed to declare node policy on blockchain"
goto end-script

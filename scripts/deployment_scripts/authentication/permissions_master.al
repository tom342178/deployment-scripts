#-----------------------------------------------------------------------------------------------------------------------
# Declare a permission that's used by the master node, which only grants those with the policy access to the `blockchain`
# database. The code is using the root private key for signing permission policy
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/permissions_master.al

:check-policy:
is_policy = blockchain get permissions where name="master node permissions" and company=!company_name
if !is_policy then goto end-script

:create-policy:
on error ignore
<new_policy = {"permissions" : {
    "name" : "master node permissions",
    "company": !company_name,
    "enable" : ["*"],
    "database": ["blockchain"]
}}>

:publish-policy:
process !local_scripts/deployment_scripts/authentication/publish_policy_root.al
if error_code == 1 then goto sign-policy-error
if error_code == 2 then goto prepare-policy-error
if error_code == 3 then declare-policy-error

:end-script:
end script

:sign-policy-error:
echo "Failed to sign permissions policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member permissions policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Failed to declare permissions policy on blockchain"
goto end-script

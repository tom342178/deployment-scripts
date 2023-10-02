#-----------------------------------------------------------------------------------------------------------------------
# Declare a generic permission, with no limitations, except `drop` command. The code is using the root private key for
# signing permission policy
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/permissions_limited_restrictions.al

:check-policy:
is_policy = blockchain get permissions where name="limited restrictions" and company=!company_name
if !is_policy then goto end-script

:create-policy:
<new_policy = {"permissions" : {
    "name" : "limited restrictions",
    "company": !company_name,
    "databases" : ["*"],
    "enable" : ["*"],
    "disable": ["drop", "system", "python", "exit", "disconnect dbms", "reset signatory", "file delete"]
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

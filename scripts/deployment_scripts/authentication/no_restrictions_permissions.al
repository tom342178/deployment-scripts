#----------------------------------------------------------------------------------------------------------------------#
# Declare permissions policy - code assumes user has run keys script
#   To run keys script: process !local_scripts/authentication/root_keys.al
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/no_restrictions_permissions.al

:validate-permission-policy:
on error ignore
permission_name = no_restrictions
is_permission = blockchain get permissions where name=!permission_name
if !is_permission then
do echo "Notice: `No Restrictions` policyy already exists"
do goto end-script


:create-policy:
<permission = {"permissions" : {
    "name" : !permission_name,
    "databases" : ["*"],
    "enable" : ["*"]
    }
}>

:sign-policy:
on error goto sign-policy-error
id sign !permission where key = !private_key and password = !root_password

:validate-policy:
on error goto validate-policy-error
test_policy = json !permission
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call publish-policy-error
blockchain prepare policy !permission
blockchain insert where policy = !permission and local = true  and master = !ledger_conn


:end-script:
end script

:sign-policy-error:
echo "Error: Failed to sign root member policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with root member policy declaration"
goto end-script

:publish-policy-error:
echo "Error: Issue with declaring policy in blockchain"
return

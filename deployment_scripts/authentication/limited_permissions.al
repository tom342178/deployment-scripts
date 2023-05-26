#----------------------------------------------------------------------------------------------------------------------#
# Declare permissions policy - code assumes user has run keys script
#   To run keys script: process !local_scripts/authentication/root_keys.al
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/limited_permissions.al

:validate-permiission-policy:
on error ignore
permission_name = limited_permissions
is_permission = blockchain get permissions where name=!permission_name
if !is_permission then
do echo "Notice: `Limited Permissions` policy already exists"
do goto end-script


:create-policy:
<permission = {"permissions" : {
    "name" : !permission_name,
    "databases" : ["*"],
    "enable" : [ "file", "get", "sql", "echo", "print", "blockchain", "event"],
    "disable" : ["system", "drop", "exit"]
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

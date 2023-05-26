#--------------------------------------------------------------------------------------------------------------------#
# Assign privileges to the node
#   To run keys script: process !local_scripts/authentication/root_keys.al
#--------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/assign_node_privileges.al

:set-params:
on error ignore
# Name of permission node should have
permission_name = no_restrictions

:get-values:
on error goto set-values-error
member_key = blockchain get member where type=node  and name = !remote_node_name and company = !remote_node_company  bring [member][public_key]
permission_id = blockchain get permissions where name=!permission_name bring [permissions][id]
if not !member_key or not !permission_id then goto set-values-error

:check-policy:
on error ignore
is_policy = blockchain get assignment where name=!remote_node_name and company=!remote_company_name
if !is_policy then goto check-policy-notice
do goto end-script

:prep-policy:
<assignment = {"assignment": {
    "name": !remote_node_name,
    "company": !remote_node_company,
    "permissions": !permission_id,
    "members": [!member_key]
    }
}>

:sign-policy:
on error goto sign-policy-error
id sign !assignment where key = !private_key and password = !root_password

:validate-policy:
on error goto validate-policy-error
test_policy = json !assignment
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call publish-policy-error
blockchain prepare policy !assignment
blockchain insert where policy = !assignment and local = true  and master = !ledger_conn

:set-auth:
on error goto set-auth-error
set node authentication on

:end-script:
end script

:set-values-error:
echo "Error: Failed to get member key for " + !remote_node_name + " and/or permission id for " + !permission_name + ", cannot continue"
goto end-script

:check-policy-notice:
echo "Notice: permissions for " + !remote_node_name + " already exists"
goto end-script

:sign-policy-error:
echo "Error: Failed to sign root member policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with root member policy declaration"
goto end-script

:publish-policy-error:
echo "Error: Issue with declaring policy in blockchain"
return

#----------------------------------------------------------------------------------------------------------------------#
# Declare root member policy - code assumes user has run keys script
#   To run keys script: process !local_scripts/authentication/root_keys.al
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/declare_root_member.al

:validate-root-user:
on error ignore
is_member = blockchain get member where type=root
if !is_member then
do echo "Notice: Root member policy already exists."
do goto end-script
else if not !root_password then
do echo "Error: Missing root_password variable, cannot continue"
do goto end-script


:create-policy:
<member = {"member" : {
    "type" : "root",
    "name"  : !root_name,
    "company": !company_name
    }
}>


:sign-policy:
on error goto sign-policy-error
id sign !member where key = !private_key and password = !root_password

:validate-policy:
on error goto validate-policy-error
test_policy = json !new_policy
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call publish-policy-error
blockchain prepare policy !member
blockchain insert where policy = !member and local = true  and master = !ledger_conn

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

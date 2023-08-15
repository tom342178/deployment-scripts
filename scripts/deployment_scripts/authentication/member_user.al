#--------------------------------------------------------------------------------------------------------
# Create member policy for a user. Each node should have its own member policy
#--------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/member_user.al

:declare-params:
on error ignore
key_name = python !user_name.replace(" ", "_").replace("-", "_").strip()

is_policy = blockchain get member where type=!user_type and name=!user_name and company=!company_name
if !is_policy then goto end-script

:clean-keys:
del_name = !id_dir + !key_name + "*"
system rm -rf !del_name

:create-keys:
on error goto create-keys-error
id create keys where password = !user_password and keys_file = !key_name

on error ignore
user_private_key = get private key where keys_file = !key_name
if not !private_key then goto private-key-error

:create-policy:
<new_policy = {"member": {
    "type" : !user_type,
    "name": !user_name,
    "company": !company_name
}}>

:prepare-policy:
on error goto prepare-policy-error
new_policy = id sign !new_policy where key = !user_private_key and password = !user_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:create-keys-error:
echo "Failed to create user keys. Cannot continue with process"
goto end-script

:private-key-error:
echo "Failed to get private key from generated user key"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member user policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for user member"
return

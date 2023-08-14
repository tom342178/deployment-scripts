#--------------------------------------------------------------------------------------------------------
# Create member policy for a user. Each node should have its own member policy
#--------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/member_user.al

:declare-params:
on error ignore
set user_name = admin
set user_password = passwd

if $NODE_PASSWORD then node_password = $NODE_PASSWORD
if $USER_NAME then user_name = $USER_NAME
if $USER_PASSWORD then user_password = $USER_PASSWORD
if $USER_TYPE == user or $USER_TYPE == admin then w = $USER_TYPE

key_name = python !user_name.replace(" ", "_").replace("-", "_").strip()

is_policy = blockchain get member where name=!user_name and company=!company_name
if !is_policy then goto end-script

:clean-keys:
del_name = !id_dir + !key_name + "*"
system rm -rf !del_name

:create-keys:
on error goto create-keys-error
id create keys where password = !node_password and keys_file = !key_name

on error ignore
private_key = get private key where keys_file = !key_name
if not !private_key then goto private-key-error
public_key = get public key where keys_file = !key_name
if not !public_key then goto public-key-error

:prepare-policy:
<new_policy = {"member': {
    "type" : !user_type,
    "name": !user_name,
    "company": !company_name,
    "public_key": !public_key
}}>

:prepare-policy:
on error goto prepare-policy-error
if !enable_auth == true then  new_policy = id sign !new_policy where key = !new_policy and password = !user_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:create-keys-error:
echo "Failed to create root keys. Cannot continue with process"
goto end-script

:private-key-error:
echo "Failed to get private key rom generated root key"
goto end-script

:public-key-error:
echo "Missing public key, cannot create valid member policy"
goto end-script

:prepare-policy-error:
echo "Failed to prepare member root policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for root member"
returns

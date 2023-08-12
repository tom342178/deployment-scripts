#--------------------------------------------------------------------------------------------------------
# Create root member policy. An AnyLog network should only have 1 root member, which is used for granting
# permissions to other users and/or nodes.
#--------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/member_root_user.al

:declare-params:
on error ignore
root_password = passwd
if $ROOT_PASSWORD  then set root_password = $ROOT_PASSWORD
policy_name = !company_name + " root policy"

:check-policy:
is_policy = blockchain get member where type=root and company=!company_name and name=!policy_name
if !is_policy then goto end-script

:clean-keys:
system rm -rf !id_dir/root_keys.pem

:create-keys:
on error goto create-keys-error
id create keys where password = !root_password and keys_file = root_keys

on error ignore
private_key = get private key where keys_file = root_keys
if not !private_key then goto private-key-error
public_key = get public key where keys_file = root_keys
if not !publc_key then goto public-key-error

:create-policy:
<new_policy = {"member": {
    "type": "root",
    "name": !policy_name,
    "company": !company_name,
    "public_key": !public_key
}}>

:prepare-policy:
on error goto prepare-policy-error
if !enable_auth == true then  new_policy = id sign !new_policy where key = !new_policy and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end-script

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

#----------------------------------------------------------------------------------------------------#
# Generate keys for the Root User
# :process:
#   1. remove content in `id_dir`
#   2. create root keys (public / private)
#   3. declare root policy
#----------------------------------------------------------------------------------------------------#

:set-params:
on error ignore
root_password = passwd
if $ROOT_PASSWORD  then set root_password = $ROOT_PASSWORD

system rm -rf !id_dir/root_keys.pem

:create-root-keys:
on error goto create-root-keys-error
id create keys where password = !root_password and keys_file = root_keys
on error goto private-key-error
private_key = get private key where keys_file = root_keys
public_key = get public key where keys_file = root_keys

:root-policy:
on error ignore
set new_policy = ""
set policy new_policy[member] = {}
set policy new_policy[member][type] = root
set policy new_policy[member][company] = !company_name

if not !public_key then goto public-key error
set policy new_policy[member][public_key] = !public_key

set policy new_policy[member][name] = !node_name
if !root_polcy_name then set policy new_policy[member][name] = !root_polcy_name


:preparepolicy:
on error goto prepare-policy-error
new_policy = id sign !new_policy where key = !new_policy and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end-script

:create-root-keys-error:
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
return

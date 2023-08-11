#----------------------------------------------------------------------------------------------------#
# Create node keys
#----------------------------------------------------------------------------------------------------#
# process !local_scripts/deployment_scripts/authentication/create_node_keys.al

:get-public-key:
on error ignore
public_key = get public key
if not !public_key then goto create-keys
if !public_key then
do process !local_scripts/deployment_scripts/authentication/node_public_key_policy.al.al
do goto end-script

:create-keys:
on error goto create-keys-error
id create keys for node where password=!node_password
goto get-public-key



:end-script:
end script

:create-keys-error:
echo "Failed to create private / public keys for node"
goto end-script
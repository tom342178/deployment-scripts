#-----------------------------------------------------------------------------------------------------------------------
# generic process to declare policy on blockchain
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/publish_policy_root.al

:set-params:
error_code = 0

if not !root_private_key then root_private_key = get private key where keys_file = root_keys
if not !root_private_key then goto private-key-error

:prepare-policy:
on error goto sign-policy-error
new_policy = id sign !new_policy where key = !root_private_key and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error ignore
blockchain prepare policy !new_policy
on error goto declare-policy-error
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:terminate-scripts:
exit scripts

:private-key-error:
echo "Failed to get private key from generated root key"
goto terminate-scripts

:sign-policy-error:
# error code 1 - failed to sign policy
error_code = 1
goto end-script

:prepare-policy-error:
# error code 2 - policy is not in the correct format
error_code = 2
goto end-script

:declare-policy-error:
# error code 3 - failed to publish policy on the blockchain
error_code = 3
goto end-script
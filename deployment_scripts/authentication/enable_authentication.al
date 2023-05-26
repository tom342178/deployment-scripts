#-----------------------------------------------------------------------------------------------------------------------
# For a node - enable authentication & set passwords
#   for details about passwords visit: https://github.com/AnyLog-co/documentation/blob/mohsen-dev/authentication.md#passwords
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/authentication/enable_authentication.al

:enable-authentication:
on error goto enable-authentication-error
set node authentication on

:set-local-password:
# local password: enables to encrypt and decrypt sensitive data that is stored on the local file system.
on error goto set-local-password-error
set local password = !node_password

:set-private-password:
# private password: enables the usage of the private key to sign policies and authenticate members
on error goto set-private-password-error
set private password = !node_password

:end-script:
end script

:enable-authentication-error:
echo "Error: Failed to enable node authentication"
goto end-script

:set-local-password-error:
echo "Error: Failed to set local password"
goto end-script

:set-private-password-error:
echo "Error: Failed to set private password"
goto end-script

#-----------------------------------------------------------------------------------------------------------------------
# Basic REST authentication - such that when executing a REST request user will need to specify name:password
# Example:
#   - Without Authentication: curl -X GET 10.0.0.1:32048 -H "command: get status" -H "User-Agent: AnyLog/1.23"
#   - With Authentication: curl -X GET 10.0.0.1:32048 -U user:password -H "command: get status" -H "User-Agent: AnyLog/1.23"
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/basic_rest_authentication.al

:set-local-password:
on error goto set-local-password-error
set local password = !node_passwd

:enable-authentication:
on error goto enable-authentication-error
set user authentication on

:set-user-password:
on error goto set-user-password-error
id add user where name=!user_name and password=!user_password and type=!user_type

:end-script:
end script

:set-local-password-error:
echo "Error: Failed to set local password for node"
goto end-script

:enable-authentication-error:
echo "Error: Failed to enable user authentication"
goto end-script

:set-user-password-error:
echo "Error: Failed to set user " + !user_name " with type " + !user_type
goto end-script


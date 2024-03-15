#-----------------------------------------------------------------------------------------------------------------------
# Basic REST authentication - such that when executing a REST request user will need to specify name:password
#
# How to run with authentication:
#   1. Set `base64` for username / password
#       AUTH=`echo -ne "$USERNAME:$PASSWORD" | base64 --wrap 0`
#   2. Execute cURL request
#       curl -X GET 127.0.0.1:32049 \
#       -H "command: get status" \
#       -H "User-Agent: AnyLog/1.23" \
#       -H "Authentication: ${AUTH}"
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/basic_rest_authentication.al

:set-params:
on error ignore

set node_password = passwd
set user_name = admin
set user_password = passwd
set user_type = admin

if $NODE_PASSWORD then node_password = $NODE_PASSWORD
if $USER_NAME then user_name = $USER_NAME
if $USER_PASSWORD then user_password = $USER_PASSWORD
if $USER_TYPE then user_type = $USER_TYPE

:set-local-password:
on error goto set-local-password-error
set local password = !node_password

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


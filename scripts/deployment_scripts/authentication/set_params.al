#-----------------------------------------------------------------------------------------------------------------------
# declare params for authentication process
# - node
# - root
# - user
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/set_params.al

on error ignore

:root-credentials:
if $ROOT_PASSWORD  then
do set root_password = $ROOT_PASSWORD
do set root_user = root
do if $ROOT_USER then set root_user = $ROOT_USER

:node-credentials:
set node_password = passwd
if $NODE_PASSWORD then node_password = $NODE_PASSWORD

:user-credentials:
if $USER_NAME then user_name = $USER_NAME
if $USER_PASSWORD then user_password = $USER_PASSWORD
user_type = user
if $USER_TYPE == admin then user_type = $USER_TYPE

if !user_name and !user_password and not !user_type then

:end-script:
end script
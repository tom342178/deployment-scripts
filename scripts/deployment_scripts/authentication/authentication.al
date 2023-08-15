#-----------------------------------------------------------------------------------------------------------------------
# "Main" for authentication process
#   -> declare authentication params
#   -> if root_password is configured, then declare root account and permissions
#   -> declare node member
#   ->
#   -> if user name and password, then declare user member policy
#   -> on a root account, associate user member policy
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/authentication.al

on error ignore

:set-params:
process !local_scripts/deployment_scripts/authentication/set_params.al

:declare-root-and-permissions:
if !root_password then
do process !local_scripts/deployment_scripts/authentication/member_root_user.al
do process !local_scripts/deployment_scripts/authentication/permissions_no_restrictions.al
do process !local_scripts/deployment_scripts/authentication/permissions_limited_restrictions.al
do process !local_scripts/deployment_scripts/authentication/permissions_master.al
do process !local_scripts/deployment_scripts/authentication/permissions_operator.al

:declare-node:
if !node_password then
do process process !local_scripts/deployment_scripts/authentication/member_node.al

:declare-user:
if !user_name and !user_password then
do process !local_scripts/deployment_scripts/authentication/member_user.al
do if !root_password then process !local_scripts/deployment_scripts/authentication/assignment_user.al



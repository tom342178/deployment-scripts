#----------------------------------------------------------------------------------------------------------------------#
# create keys for node
# if so:
#   - validate there's root password
#   - check if keys exist
#   - if not create them
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/node_keys.al

id_created = false
:validate-credentials:
if not !node_password then
do echo "Notice - missing node password, cannot continue" 
do goto end-script 

:get-keys:
on error ignore
private_key_node = get private key where password = !node_password  and keys_file = node_id
if not !private_key_node and !id_created == false then goto declare-keys
else if not !private_key_node and !id_created == true then goto declare-keys-error
else if !private_key_node then goto end-script 


:declare-keys:
on error goto declare-keys-error
id create keys for node where password = !node_password
id_created = true
goto get-keys

:end-script:
end script

:declare-keys-error:
echo "Error: Failure in creating private / public keys with a password value"
goto end-script

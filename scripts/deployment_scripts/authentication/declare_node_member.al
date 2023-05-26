#----------------------------------------------------------------------------------------------------------------------#
# Declare node member policy - code assumes user has run keys script
#   To run keys script (on the node being added): process !local_scripts/authentication/node_keys.al
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/declare_node_member.al

:get-node-id:
on error goto get-node-id-error
remote_node_id = run client (!remote_node_conn) get node id

:create-policy:
<member = {"member" : {
    "type" : "node",
    "name"  : !remote_node_name,
    "company": !remote_node_company,
    "public_key": !remote_node_id
    }
}>

:validate-policy:
on error goto validate-policy-error
test_policy = json !new_policy
if !test_policy == false then goto validate-policy-error

:publish-policy:
on error call publish-policy-error
blockchain prepare policy !member
blockchain insert where policy = !member and local = true  and master = !ledger_conn

:end-script:
end script

:get-node-id-error:
echo "Error: Failed to get Node ID for " + !remote_node_conn + " unable to declare policy."
goto end-script

:sign-policy-error:
echo "Error: Failed to sign root member policy"
goto end-script

:validate-policy-error:
echo "Error: Issue with root member policy declaration"
goto end-script

:publish-policy-error:
echo "Error: Issue with declaring policy in blockchain"
return
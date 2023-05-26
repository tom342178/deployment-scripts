#-----------------------------------------------------------------------------------------------------------------------
# Rest Query Node
#   --> delete blockchain file
# Note - there's no need to reset system_query (by default) as data does not need to be persistent
# <---------            Restarting Master Node        --------->
# Steps to restart master node:
#   1) declare query node: process !local_scripts/deployment_scripts/declare_generic_policy.al
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_query.al

:remove-local-blockchain:
on error call remove-local-blockchain-error
blockchain delete local file

:end-script:
end script

:remove-local-blockchain-error:
echo "Error: Failed to drop local file copy of blockchain"
return

#-----------------------------------------------------------------------------------------------------------------------
# Rest publisher Node
#   --> exit publisher
#   --> delete blockchain file
#   --> reset databases
        --> call process that reset almgm database
# <---------            Restarting publisher Node        --------->
# Steps to restart publisher node:
#   2) Declare publisher policy: process !local_scripts/deployment_scripts/declare_publisher.al
#   3) Execute `run publisher`: process !local_scripts/deployment_scripts/deploy_publisher.al
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_publisher.al

:exit-publisher:
on error call exit-publisher-error
exit publisher

:remove-local-blockchain:
on error call remove-local-blockchain-error
blockchain delete local file

:reconnect-dbms:
on error ignore
process !local_scripts/reset_node/reset_almgm.al

:end-script:
end script

:exit-publisher-error:
echo "Error: Failed to stop publisher process"
return

:remove-local-blockchain-error:
echo "Error: Failed to drop local file copy of blockchain"
return
#-----------------------------------------------------------------------------------------------------------------------
# Rest Master Node
#   --> recreate table ledger
#   --> delete blockchain file
# <---------            Restarting Master Node        --------->
# Steps to restart master node:
#   1) declare master node: process !local_scripts/deployment_scripts/declare_generic_policy.al
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/reset_scripts/reset_master.al

:drop-blockchain:
on error call drop-blockchain-error
is_table = info table blockchain ledger exists
if !is_table == true then drop table ledger where dbms = blockchain

:remove-local-blockchain:
on error call remove-local-blockchain-error
blockchain delete local file

:create-ledger-table:
on error call create-ledger-table-error
create table ledger where dbms = blockchain


:end-script:
end script

:drop-blockchain-error:
echo "Error: Failed to drop table ledger from blockchain database"
is_table = false
return

:remove-local-blockchain-error:
echo "Error: Failed to drop local file copy of blockchain"
return

:create-ledger-table-error:
echo "Error: Failed to create ledger table on blockchain database"
return
#----------------------------------------------------------------------------------------------------------------------#
# Connect to an actual blockchain as opposed to connecting to an AnyLog master
#   --> validate keys and credentials exists are set
#   --> declare / connect to blockchain account
#   --> set contract
#   --> set account
#   --> sync from contract
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/connect_blockchain.al

if !debug_mode == true then set debug on

on error ignore

if !blockchain_source == master then goto run-blockchain-sync

:blockchain-connect:
if !debug_mode == true then print "Connect to optimism"
on error goto connect-blockchain-account-error
blockchain connect to !blockchain_source where provider=!provider

# create an account - this would create public and private key
# blockchain create account optimism

:declare-blockchain-account:
if !debug_mode == true then print "Declare blockchain account"

on error goto declare-blockchain-account-error
<blockchain set account info where
    platform = !blockchain_source and
    private_key = !private_key and
    public_key = !public_key and
    chain_id = !chain_id>


:create-contract:
if !debug_mode == true then print "Create a new smart contract"

if not !contract then
do on error goto create-contract-error
do contract = blockchain deploy contract where  platform = !blockchain_source and public_key = !public_key
do print "New Contract created: " !contract " - make sure to save contract / update config file accordingly"

:blockchain-account:
 if !debug_mode == true then print "Set blockchain account information"

on error goto blockchain-account-error
blockchain set account info where platform = !blockchain_source and contract = !contract

# :blockchain-seed:
# if !debug_mode == true then print "Copy blockchain to local node"

# on error call blockchain-seed-error
# blockchain checkout from !blockchain_source

:run-blockchain-sync:
if !blockchain_source == master then
<do run blockchain sync where
    source=!blockchain_source and
    time=!blockchain_sync and
    dest=!blockchain_destination and
    connection=!ledger_conn>
<else run blockchain sync where
    source = blockchain and
    time = !blockchain_sync and
    dest=!blockchain_destination and
    platform = !blockchain_source>

:end-script:
if !blockchain_source != master then get platforms
end script

:terminate-scripts:
exit scripts

:connect-blockchain-account-error:
print "Failed to connect to Optimism"
goto terminate-scripts

:create-contract-error
print "Failed to create new contract"
goto terminate-scripts

:declare-blockchain-account-error:
print "Failed to declare account information, cannot continue..."
goto  terminate-scripts

:blockchain-seed-error:
echo "Failed to seed from blockchain"
return
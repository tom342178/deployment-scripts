#----------------------------------------------------------------------------------------------------------------------#
# Connect to an actual blockchain as opposed to connecting to an AnyLog master
#   --> validate keys and credentials exists are set
#   --> declare / connect to blockchain account
#   --> set contract
#   --> set account
#   --> sync from contract
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/connect_blockchain.al

on error ignore

:validate-params:
if !debug_mode.int == 2 then
do set debug interactive
do print "Validate keys and credentials params are declared"

if not !private_key or not !public_key or not !private_key and not chain_id then
do print "Missing private / public keys and/or chain id. Cannot setup a blockchain connectivity..."
do goto  terminate-scripts

if !debug_mode.int == 2 then
do set debug interactive
do print "Double check source is blockchain"

if !blockchain_source != blockchain then
do echo "Setting source to `blockchain`"
do set blockchain_source = blockchain

:declare-blockchain-account:
if !debug_mode.int == 2 then
do set debug interactive
do print "Declare blockchain account"

on error goto declare-blockchain-account-error
<blockchain set account info where
    platform = !platform and
    private_key = !private_key and
    public_key = !public_key and
    chain_id = !chain_id>

:create-contract:
if !debug_mode.int == 2 then
do set debug interactive
do print "Get blockchain contract ID - if a contract does not exist, code will automatically create one"

on error goto create-contract-error
contract = blockchain deploy contract where  platform = !platform and public_key = !public_key

:blockchain-account:
if !debug_mode.int == 2 then
do set debug interactive
do print "Set blockchain account information"

on error goto blockchain-account-error
blockchain set account info where platform = !platform and contract = !contract

:blockchain-seed:
if !debug_mode.int == 2 then
do set debug interactive
do print "Copy blockchain to local node"

on error call blockchain-seed-error
blockchain checkout from !platformm

:blockchain-sync:
if !debug_mode.int == 2 then
do set debug interactive
do print "set blockchain sync"

on error call blockchain-sync-error
<run blockchain sync where
    source = !blockchain_source and
    time = !sync_time and
    dest = !blockchain_destination and
    platform = !platform>

:end-script:
end script

:terminate-scripts:
exit scripts

:declare-blockchain-account-error:
print "Failed to declare account information, cannot continue..."
goto  terminate-scripts

:create-contract-error:
print "Failed to generate contract for the blockchain, cannot continue..."
goto  terminate-scripts

:blockchain-account-error:
print "Failed to set account information, cannot continue..."
goto  terminate-scripts

:blockchain-seed-error:
echo "Failed to seed from blockchain"
return
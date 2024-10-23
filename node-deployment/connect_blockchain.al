#----------------------------------------------------------------------------------------------------------------------#
# Connect to an actual blockchain as opposed to connecting to an AnyLog master
#   --> validate keys and credentials exists are set
#   --> declare / connect to blockchain account
#   --> set contract
#   --> set account
#   --> sync from contract
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/connect_blockchain.al

reset error log
on error ignore

:blockchain-connect:
if !debug_mode.int == 2 then
do set debug interactive
do print "Connect to optimism"
on error goto connect-blockchain-account-error
blockchain connect to optimism where provider=!provider

# create an account - this would create public and private key
# blockchain create account optimism

:declare-blockchain-account:
if !debug_mode.int == 2 then
do set debug interactive
do print "Declare blockchain account"

on error goto declare-blockchain-account-error
<blockchain set account info where
    platform = optimism and
    private_key = !private_key and
    public_key = !public_key and
    chain_id = !chain_id>

# create a new smart contract
# contract = blockchain deploy contract where  platform = optimism and public_key = !public_key

:blockchain-account:
if !debug_mode.int == 2 then
do set debug interactive
do print "Set blockchain account information"

on error goto blockchain-account-error
blockchain set account info where platform = optimism and contract = !contract

:blockchain-seed:
if !debug_mode.int == 2 then
do set debug interactive
do print "Copy blockchain to local node"

on error call blockchain-seed-error
blockchain checkout from optimism

:end-script:
get platforms
end script

:terminate-scripts:
exit scripts

:connect-blockchain-account-error:
print "Failed to connect to Optimism"
goto terminate-scripts

:declare-blockchain-account-error:
print "Failed to declare account information, cannot continue..."
goto  terminate-scripts

:blockchain-seed-error:
echo "Failed to seed from blockchain"
return
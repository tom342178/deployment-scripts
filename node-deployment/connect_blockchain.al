#----------------------------------------------------------------------------------------------------------------------#
#
#----------------------------------------------------------------------------------------------------------------------#
on error ignore

:validate-params:
if not !private_key or not !public_key or not !private_key and not chain_id then
do print "Missing private / public keys and/or chain id. Cannot setup a blockchain connectivity..."
do goto  terminate-scripts
if !blockchain_source != blockchain then
do print "Blockchain source is not configured properly, cannot continue..."
do goto  terminate-scripts

:declare-blockchain-account:
on error goto declare-blockchain-account-error
on error goto set-account-error
<blockchain set account info where
    platform = !platform and
    private_key = !private_key and
    public_key = !public_key and
    chain_id = !chain_id>

:create-contract:
on error goto create-contract-error
contract = blockchain deploy contract where  platform = !platform and public_key = !public_key

:blockchain-account:
on error goto blockchain-account-error
blockchain set account info where platform = !platform and contract = !contract

:blockchain-seed:
on error call blockchain-seed-error
blockchain seed from !contract

:blockchain-sync:
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
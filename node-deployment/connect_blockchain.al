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

:set-params:
public_key = 0xdf29075946610ABD4FA2761100850869dcd07Aa7
private_key = 712be5b5827d8c111b3e57a6e529eaa9769dcde550895659e008bdcf4f893c1c
contract = 0x8fD816a62e8E7985154248019520915778eB4013
chain_id = 11155420
provider = https://optimism-sepolia.infura.io/v3/532f565202744c0cb7434505859efb74

blockchain connect to optimism where provider=!provider

# blockchain create account optimism

blockchain set account info where platform = optimism and private_key = !private_key and public_key = !public_key and chain_id = !chain_id

get platforms

# contract = blockchain deploy contract where  platform = optimism and public_key = !public_key

blockchain set account info where platform = optimism and contract = !contract

run blockchain sync where source = blockchain and time = !blockchain_sync and dest = file and platform = optimism



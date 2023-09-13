#-----------------------------------------------------------------------------------------------------------------------
# based on blockchain get license_key and company name
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/set_params_blockchain.al

:blockchain-seed:
# validate if blockchain exists or not
is_blockchain = blockchain test
if !is_blockchain == true then goto get-params
if !is_blockchain == false and !node_type == master then goto end-script
if !is_blockchain == false and !seed_count == 1 then goto blockchain-seed-error

# get blockchain using `blockchain seed` command
if !is_blockchain == false and !ledger_conn then
do blockchain seed from !ledger_conn
do seed_count = 1
do goto get-seed

:get-params:
# using the master node policy, get needed information
master_policy = blockchain get master bring.first
if !master_policy then
do if not !company_name then company_name = from !master_policy bring [*][company]
do if not !license_key then  license_key = from !master_policy bring [*][license]
do ledger_conn = blockchain get master bring.ip_port

# check if policy already exists (based on company and name), if so - use its values rather than defaults
policy = blockchain get !node_type where company=!company_name and name=!node_name
if !policy then
do anylog_server_port = from !policy bring [*][port]
do anylog_rest_port = from !policy bring [*][rest_port]
do anylog_broker_port = from !policy bring [*][broker_port]

:validate-params:
# validate if license and company exist
if not !license_key then goto missing-license-key
if not !company_name then goto missing-company-name

:end-script:
end script

:terminate-scripts:
end scripts

:blockchain-seed-error:
echo "Failed to get information from ledger conn"
goto validate-params

:missing-license-key:
print "Missing license key, cannot continue..."
goto terminate-scripts

:missing-company-name:
print "Missing company name, cannot continue..."
goto terminate-scripts





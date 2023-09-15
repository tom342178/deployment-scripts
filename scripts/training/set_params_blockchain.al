#-----------------------------------------------------------------------------------------------------------------------
# based on blockchain get license_key and company name
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/training/set_params_blockchain.al

on error ignore
reset error log

:blockchain-seed:
on error goto blockchain-seed-error
blockchain seed from !ledger_conn

:blockchain-test:
# validate if blockchain exists or not
on error ignore
is_blockchain = blockchain test
if !is_blockchain == true then goto get-params
if !is_blockchain == false and !node_type == master then goto validate-params
if !is_blockchain == false then goto blockchain-seed-error

:get-params:
# using the master node policy, get needed information
is_master = blockchain get master
if !is_master and not !company_name then company_name = blockchain get master bring [*][company]
if !is_master and not !license_key then license_key = blockchain get master bring [*][license]
if !is_master then ledger_conn = blockchain get master bring.ip_port

# check if policy already exists (based on company and name), if so - use its values rather than defaults
policy = blockchain get !node_type where company=!company_name and name=!node_name and ip=!external_ip and internal_ip=!ip
if !policy then
do server_port = blockchain get !node_type where company=!company_name and name=!node_name and ip=!external_ip and internal_ip=!ip bring [*][port]
do rest_port = blockchain get !node_type where company=!company_name and name=!node_name and ip=!external_ip and internal_ip=!ip   bring [*][rest_port]
do broker_port = blockchain get !node_type where company=!company_name and name=!node_name and ip=!external_ip and internal_ip=!ip bring [*][broker_port]

if !server_port then anylog_server_port = !server_port
if !rest_port then anylog_rest_port = !rest_port
if !broker_port then anylog_broker_port = !broker_port

:validate-params:
# validate if license and company exist
if not !license_key then goto missing-license-key
if not !company_name then goto missing-company-name

:end-script:
end script


:terminate-scripts:
exit scripts

:blockchain-seed-error:
print "Failed to execute blockchain seed"
goto terminate-scripts

:missing-license-key:
print "Missing license key, cannot continue..."
goto terminate-scripts

:missing-company-name:
print "Missing company name, cannot continue..."
goto terminate-scripts



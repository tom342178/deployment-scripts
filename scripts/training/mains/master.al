#----------------------------------------------------------------------------------------------------------------------#
# Prepare for deployment of a master node policy
# :process:
#   1. declare node name / node type (in main)
#   2. declare company name, license and ports (optional)
#   3. format LEDGER_CONN based on TCP service port and IP
#   4. declare init policy for master
#   5.
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/training/generic_policies/mains/master.al

:set-params:
set anylog_server_port = 32048
set anylog_rest_port = 32049

if $COMPANY_NAME then set company_name = $COMPANY_NAME
else company_name = blockchain get master bring [*][company]
if $LICENSE_KEY then set license_key = $LICENSE_KEY
else license_key = blockchain get master bring [*][license]

if $ANYLOG_SERVER_PORT then set anylog_server_port=$ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then set anylog_rest_port=$ANYLOG_REST_PORT

ledger_conn = !ip + : + !anylog_server_port

if not !license_key then goto missing-license-key
if not !company_name then goto goto missing-company-name

:set-policy:
on error ignore
process !local_scripts/training/generic_policies/generic_master_policy.al


:execute-license:
on error call license-error
set license where activation_key=!license_key

:end-script:
end script

:terminate-scripts:
end scripts

:missing-license-key:
print "Missing license key, cannot continue..."
goto terminate-scripts

:missing-company-name:
print "Missing company name, cannot continue..."
goto terminate-scripts


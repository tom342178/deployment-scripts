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

policy_id = blockchain get config where node_type = !node_type bring [*][id]
on error call config-from-policy-error
if !policy_id then config from policy where id = !policy_id

:execute-license:
on error call license-error
set license where activation_key=!license_key

:end-script:
end script

:terminate-scripts:
end scripts

:missing-license-key:
print "Missing license key, cannot continue..."
goto end-script

:missing-company-name:
print "Missing company name, cannot continue..."
goto end-script


:license-error:
print "Failed to set license key..."
goto end-script


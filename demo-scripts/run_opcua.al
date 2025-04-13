#----------------------------------------------------------------------------------------------------------------------#
# Sample deployment process for OPC-UA
# https://github.com/AnyLog-co/documentation/blob/master/opcua.md
# :steps:
#   1. create OPC-UA policies
#   2. declare policies
#   3. create OPC-UA call
#   4. start OPC-UA service
#----------------------------------------------------------------------------------------------------------------------#
# process !anylog_path/deployment-scripts/demo-scripts/run_opcua.al


:create-policy:
on error goto create-policy-error
<get opcua struct where
    url = !opcua_url and
    node = !opcua_node and
    dbms = !default_dbms and
    format = policy  and
    schema = true and
    class = variable and
    target = "local = true and master = !ledger_conn" and
    output = !tmp_dir/opcua_policies.al>

on error ignore
process !tmp_dir/opcua_policies.al

:opcua-service:
on error goto opcua-service-error
<get opcua struct where
    url = !opcua_url and
    node = !opcua_node and
    dbms = !default_dbms and
    frequency = !opcua_frequency and
    format = run_client  and
    class = variable and
    name=opcua-client1 and
    output = !tmp_dir/run_opcua_service.al>

on error ignore
process !tmp_dir/run_opcua_service.al

get opcua client
:end-script:
end script

:create-policy-error:
print "Failed to create OPC-UA policies"
goto end-script

:opcua-service-error:
print "Failed to start OPC-UA service"
goto end-script
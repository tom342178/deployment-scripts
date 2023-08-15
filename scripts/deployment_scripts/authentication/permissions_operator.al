#-----------------------------------------------------------------------------------------------------------------
# Declare a generic permission for an Operator node
#-----------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/authentication/permissions_operator.al

:set-params:
on error ignore
root_user = admin
root_password = passwd
if $ROOT_PASSWORD  then set root_password = $ROOT_PASSWORD
if $ROOT_USER then root_user = $ROOT_USER

:check-policy:
is_policy = blockchain get permissions where name="operator node restrictions" and company=!company_name
if !is_policy then goto end-script

:create-policy:
<new_policy = {"permissions" : {
    "name" : "operator node restrictions",
    "company": !company_name,
    "databases" : ["almgm", '!default_dbms'],
    "enable" : ["*"]
}}>

:prepare-policy:
on error goto prepare-policy-error
new_policy = id sign !new_policy where key = !new_policy and password = !root_password
validate_policy = json !new_policy
if not !validate_policy then goto prepare-policy-error

:declare-policy:
on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

:end-script:
end script

:prepare-policy-error:
echo "Failed to prepare member root policy for publishing on blockchain"
goto end-script

:declare-policy-error:
echo "Error: Failed to declare policy for root member"
return
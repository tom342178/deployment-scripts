#-----------------------------------------------------------------------------------------------------------------------
# Script to deploy a policy with license information
#
# ---- Sample Policy ---
# {'license' : {
#       'owner' : 'AnyLogCo.',
#       'company' : 'AnyLog Co.',
#       "expiration": "2025-03-01",
#       "activation_key": "af043d39675e85e5c9d74999dfd123de2e54e6ed4f1fe9bed04b8ce7754826c89aa1adfb562b18d49f7c4a336ece
#                          dadb3c3ca43f88a7d3f4644b6424c5f6ba9217bede0bbcdc94094af9f6e213aa247ccb3ed5f77b794f68df07a6255
#                          2ac0c6d9c67e406fe6213d6145d7c3d2c127e99906dffebd1c34c12b259719d80e6fcb3{
#                           'company':'AnyLogCo.',
#                           'expiration':'2025-03-01',
#                           'type':'beta'
#                          }",
#       'id' : '0015392622f3eaac70eafa4311fc2338',
#       'date' : '2022-06-04T22:47:48.479532Z',
#       'status' : 'active',
#       'ledger' : 'global'
# }}
# ---- Sample Policy ---
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/policies/declare_cluster_policy.al

:set-params:
on error ignore
if $LICENSE_KEY and not !license_key then license_key = $LICENSE_KEY
if not !license_key and not goto missing-license-key

owner = from !license_key bring [company]
expiration = from !license_key bring [expiration]

set create_license = false

:check-policy:
if !debug_mode == true then print "Check whether license policy exists"

on error ignore
activation_key =  blockchain get license where owner = !owner and expiration >= now().date bring [license][activation_key]
if not !activation_key and !create_license == true then goto declare-policy-error
if !activation_key then goto set-license

:create-license:
if !expiration < now().date then goto expiration-error
on error ignore
<new_policy = {
    "license": {
        "company': !company_name,
        "owner": !owner,
        "expiration": !expiration
        "activation_key": !license_key"
    }
}>

:publish-policy:
if !debug_mode == true then print "Declare policy on blockchain"

process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error
set create_cluster = true

goto check-policy

:set-license:
on error goto set-license-error
set license where activation_key = !activation_key

:end-script:
end script

:terminate-scripts:
exit scripts

:missing-license-key:
print "missing license key, cannot create policy / activate node"
goto terminate-scripts

:expiration-error:
print "License key expiration date is older them today, cannot create policy / activate node"
goto terminate-scripts

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts

:set-license-error:
print "Failed to active node using the license key"
goto terminate-scripts

:policy-error:
print "Failed to publish policy for an unknown reason"
goto terminate-scripts



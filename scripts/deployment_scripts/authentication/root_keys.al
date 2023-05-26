#----------------------------------------------------------------------------------------------------------------------#
# create keys for root user
# if so:
#   - validate there's root password
#   - check if keys exist
#   - if not create them
#
# Sample Policy
#  {"member": {
#    "type": "root",
#    "name": "admin",
#    "company": "New Company",
#    "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCzrKmV/mf0oA1WvkqJ5F+SxAz/"
#                  "mpJfoJPTkKUwbVNZmC+CCHGMnvbw3eN+EKM6rTosN/HUrzUIi2m6K4ZVv+MfKWYY"
#                  "VPVewGsDXXK0Endbou/01dljVyM6p7aqrTtutGJb8hJUZDxn+MxxKOASHgXb5kgK"
#                  "bJHGcCaa5uJEBTwBfQIDAQAB",
#    "id": "16ec124e46d5792dc28fc1b5dedd4b02",
#    "date": "2023-01-10T19:55:40.247276Z",
#    "signature": "48ac358d526f3e2306818b7eff22d061dd2930dee91669f6797c046baebb88d8"
#                 "5033d167e98df1fb36c82feb6a17892e0ad69841fe4e1d4189e25b8e0875e400"
#                 "a4916886f432206200c9c877cc233ac8eb2f1d77ac59f66bf31e186322be7365"
#                 "9e4eca91d3d8a6cc268f4d5fa7c7cd2dedb6011d35c251dab194eeea2d980b5f",
#  "ledger": "global"
#}}
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/authentication/root_keys.al

id_created = false
:check-root:
# check whether this is the root user or not
on error ignore
is_member = blockchain get member where type=root
if not !is_member and not !root_password then goto disable-auth
else if !is_member and not !root_password then
do echo "Notice: root member already exists on the network. Please contact your administrator for access"
do goto end-script
else if !is_member and !root_password then echo "Notice - this is the root member node"


:get-keys:
on error ignore
private_key = get private key where password = !root_password  and keys_file = root_key
if not !private_key and !id_created == true then goto declare-keys-error
else if !private_key and !id_created == true then goto end-script

:declare-keys:
on error call declare-keys-error
id create keys where password = !root_password and keys_file = root_key
id_created = true
goto get-keys


:end-script:
end script

:disable-auth:
echo "Notice: Missing root password, cannot create root credentials. Setting enable_auth to False"
set enable_auth = false
goto end-script

:declare-keys-error:
echo "Error: Failure in creating private / public keys with a password value"
set root_password_set = false
goto end-script

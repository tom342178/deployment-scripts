#----------------------------------------------------------------------------------------------------------------------#
# Issue: when setting `set debug on` in a script, I expect to see the command `print` being called
#----------------------------------------------------------------------------------------------------------------------#
set debug on
on error ignore

<new_policy = {"my_policy": {
    "name": "test-policy",
    "company": "AnyLog",
    "script": [
        "set debug on",
        "print hello world"
    ]
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true

policy_id = blockchain get my_policy bring [*][id]
config from policy where id = !policy_id

#----------------------------------------------------------------------------------------------------------------------#
# Expect:
# Actual
# AL litsanleandro-operator1 +> [0007] on error ignore --> ON ERROR IGNORE
# AL litsanleandro-operator1 +> [0016] new_policy = {"my_policy": { "name": "test-policy", "company": "AnyLog", "script": [ "set debug on", "print hello world" ] }} --> Success
# AL litsanleandro-operator1 +> [0018] blockchain prepare policy !new_policy --> Success
# AL litsanleandro-operator1 +> [0019] blockchain insert where policy=!new_policy and local=true --> Success
# AL litsanleandro-operator1 +> [0021] policy_id = blockchain get my_policy bring [*][id] --> Success
# AL litsanleandro-operator1 +>
# set debug on  --> success
# print hello world --> success
# 'hello world'
#
# AL litsanleandro-operator1 +>
# |=============================================================|
# |Script from policy 13f00e7a480da592d1b8d6a6f359d484 processed|
# |=============================================================|
# AL litsanleandro-operator1 +> [0022] config from policy where id = !policy_id --> Success
#----------------------------------------------------------------------------------------------------------------------#
# Actual:
# AL litsanleandro-operator1 +> [0007] on error ignore --> ON ERROR IGNORE
# AL litsanleandro-operator1 +> [0016] new_policy = {"my_policy": { "name": "test-policy", "company": "AnyLog", "script": [ "set debug on", "print hello world" ] }} --> Success
# AL litsanleandro-operator1 +> [0018] blockchain prepare policy !new_policy --> Success
# AL litsanleandro-operator1 +> [0019] blockchain insert where policy=!new_policy and local=true --> Success
# AL litsanleandro-operator1 +> [0021] policy_id = blockchain get my_policy bring [*][id] --> Success
# AL litsanleandro-operator1 +>
# 'hello world'
#
# AL litsanleandro-operator1 +>
# |=============================================================|
# |Script from policy 13f00e7a480da592d1b8d6a6f359d484 processed|
# |=============================================================|
# AL litsanleandro-operator1 +> [0022] config from policy where id = !policy_id --> Success
#----------------------------------------------------------------------------------------------------------------------#
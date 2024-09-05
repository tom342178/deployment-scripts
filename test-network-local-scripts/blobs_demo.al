# process !root_path/deployment-scripts/test-network-local-scripts/blobs_demo.al
on error ignore

:declare-params:
set is_demo = true
car_policy = car-videos
factory_policy = factory-imgs
people_policy = people-videos

:declare-policies:
process !root_path/deployment-scripts/demo-scripts/blobs_car_videos.al
process !root_path/deployment-scripts/demo-scripts/blobs_factory_images.al
process !root_path/deployment-scripts/demo-scripts/blobs_people_videos.al

:msg-clien:
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!car_policy and
    policy=!car_policy
) and topic = (
    name=!factory_policy and
    policy=!factory_policy
) and topic =(
    name=!people_policy and
    policy=!people_policy
)>
if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!car_policy and
    policy=!car_policy
) and topic = (
    name=!factory_policy and
    policy=!factory_policy
) and topic =(
    name=!people_policy and
    policy=!people_policy
)>
if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=!car_policy and
    policy=!car_policy
) and topic = (
    name=!factory_policy and
    policy=!factory_policy
) and topic =(
    name=!people_policy and
    policy=!people_policy
)>
#----------------------------------------------------------------------------------------------------------------------#
# Set parameters for AnyLog, based on values in master node policy
# :required-params:
#   -> node_type
#   -> node_name
# :from master:
#   -> company_name
#   -> license_key
# :optional_params:
#   -> server and rest ports
#----------------------------------------------------------------------------------------------------------------------#

is_master = blockchain get master
if !is_master then
do company_name = blockchain get master bring [*][company]
do license_key = blockchain get master bring [*][license]
else if $LICENSE_KEY then license_key = $LICENSE_KEY

if !node_type == generic then
do set anylog_server_port = 32548
do set anylog_rest_port = 32549
do set anylog_broker_port = 32550

else if !node_type == operator then
do set anylog_server_port = 32148
do set anylog_rest_port = 32149
do set anylog_broker_port = 32149
do if $DEFAULT_DBMS then set default_dbms = $d

else if !node_type == query then
do set anylog_server_port = 32348
do set anylog_rest_port = 32349

else if !node_type == publisher then
do set anylog_server_port = 32248
do set anylog_rest_port = 32249

if $ANYLOG_SERVER_PORT then set anylog_server_port=$ANYLOG_SERVER_PORT
if $ANYLOG_REST_PORT then set anylog_rest_port=$ANYLOG_REST_PORT
if $ANYLOG_BROKER_PORT then set anylog_rest_port=$ANYLOG_REST_PORT

:end-script:
end script
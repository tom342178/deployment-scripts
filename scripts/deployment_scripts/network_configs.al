#-----------------------------------------------------------------------------------------------------------------------
# Set network configuration
# --> TCP
# --> REST
# --> BROKER (if set)
# If an overlay_ip is declared, it wil be used as the local IP
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/network_configs.al

set debug off
set enable_overlay = false
if !overlay_ip then set enable_overlay = true

:policy-based-networking:
if !policy_based_networking == true then
do set new_policy = ""
do process !local_scripts/deployment_scripts/policies/declare_network_config_policy.al
do goto query-pool

:tcp-networking:
on error goto tcp-networking-error
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

if !overlay_ip then set enable_overlay = true
:rest-networking:
on error goto rest-networking-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

if not !anylog_broker_port then goto end-script 

if !overlay_ip then set enable_overlay = true
:broker-networking:
on error goto broker-networking-error
<run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>

:query-pool:
# set query pool if different from default.
on error goto query-pool-error
if !query_pool != 3 then
do exit workers
do sleep 5
do set query pool !query_pool


:end-script:
end script

:terminate-scripts:
exit scripts

:policy-based-networking-error:
echo "Error: Failed to connect to network with Policy ID " !policy_id ". Cannot continue..."
goto terminate-scripts

:policy-based-networking-notice:
echo "Error: Failed to locate Policy ID for connecting to network. Cannot continue..."
goto terminate-scripts

:tcp-networking-error:
if !overlay_ip then echo
do "Error: Failed to connect to TCP with overlay IP address - reattempt without an overlay IP address"
do enable_overlay = false
do goto tcp-networking
else
do echo "Error: Failed to connect to TCP with IP address - unable to continue deployment process"
do goto terminate-scripts

:rest-networking-error:
if !overlay_ip then echo
do "Error: Failed to connect to REST with overlay IP address - reattempt without an overlay IP address"
do enable_overlay = false
do goto rest-networking
else
do echo "Error: Failed to connect to REST with IP address - unable to continue deployment process"
do goto terminate-scripts

:broker-networking-error:
if !overlay_ip then echo
do "Error: Failed to connect to Message Broker with overlay IP address - reattempt without an overlay IP address"
do enable_overlay = false
do broker-networking
else
do echo "Error: Failed to connect to Message Broker with IP address - will continue deployment without Message Broker"
do goto query-pool

:query-pool-error:
echo "Failed to exit or changed query pool counter"
goto exit-script

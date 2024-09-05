#----------------------------------------------------------------------------------------------------------------------#
# Connect to TCP, REST and Broker (if configured) using default params
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/connect_networking.al

on error ignore
if !overlay_ip then goto overlay-tcp-networking

:tcp-networking:
on error goto tcp-networking-error
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

:rest-networking:
on error goto rest-networking-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

if not !anylog_broker_port then goto end-script

:broker-networking:
on error goto broker-networking-error
<run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>
 goto end-script


:overlay-tcp-networking:
on error goto tcp-networking-error
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

:overlay-rest-networking:
on error goto rest-networking-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!overlay_ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

if not !anylog_broker_port then goto end-script

:overlay-broker-networking:
on error goto broker-networking-error
<run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!!overlay_ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>
 goto end-script

:end-script:
end script

:terminate-scripts:
exit scripts

:tcp-networking-error:
print "Error: Failed to connect to TCP with IP address - unable to continue deployment process"
goto terminate-scripts

:rest-networking-error:
print "Error: Failed to connect to REST with IP address - unable to continue deployment process"
goto terminate-scripts

:broker-networking-error:
print "Error: Failed to connect to Message Broker with IP address - will continue deployment without Message Broker"
do goto terminate-scripts





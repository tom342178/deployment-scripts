#-----------------------------------------------------------------------------------------------------------------------
# Set network configuration
# --> TCP
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/network_configs.al

on error goto tcp-networking-error
<if !overlay_ip then run tcp server where
    external_ip = !external_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

<if not !overlay_ip then run tcp server where
    external_ip = !external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

:end-script:
end script

:terminate-scripts:
end scripts


:tcp-networking-error:
echo "Error: Failed to connect to TCP with IP address - unable to continue deployment process"
goto terminate-scripts

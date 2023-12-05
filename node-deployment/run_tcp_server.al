#----------------------------------------------------------------------------------------------------------------------#
# TCP connection temporarily used in order to get the initial blockchain configs
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/deployment_scripts/run_tcp_server.al

:tcp-networking:
on error goto tcp-networking-error
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=3>

:end-script:
end script

:terminate-scripts:
end scripts

:tcp-networking-error:
print "Error: Failed to connect to TCP with IP address - unable to continue deployment process"
goto terminate-scripts





#-----------------------------------------------------------------------------------------------------------------------
# Deployment code for setting streamer and buffer configs
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/deployment_scripts/pre_deployment.al

:set-buffer:
on error call buffer-threshold-error
set buffer threshold where time=!threshold_time and volume=!threshold_volume and write_immediate=!write_immediate

:set-stream:
on error call streamer-error
run streamer

:end-script:
end script

:buffer-threshold-error:
echo "Error: Failed to set buffer threshold"
return

:streamer-error:
echo "Error: Failed to start streamer"
return



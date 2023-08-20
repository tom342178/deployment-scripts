#-----------------------------------------------------------------------------------------------------------------------
# Prepare an empty node to be used for testing
#   1. set directories
#   2. set license key
#-----------------------------------------------------------------------------------------------------------------------
# process !local_scripts/run_scripts/start_empty_node.al

:directories:
on error ignore
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

:create-directories:
on error goto create-directories-error
create work directories

:set-license:
on error goto set-license-error
if $LICENSE_KEY then set license where activation_key = $LICENSE_KEY

:end-script:
end script

:create-directories-error:
print "Failed to create work directories"
goto end-script

:set-license-error:
print "Failed to set license key. License key must be set for any other commands to be executed"
goto end-script

#----------------------------------------------------------------------------------------------------------------------#
# Main for generic scripts
#   -> set directory structure
#   -> set configs
#   -> declare policies
#   -> execute based on node type
#----------------------------------------------------------------------------------------------------------------------#
# python3 /app/AnyLog-Network/anylog.py process $ANYLOG_PATH/deployment-scripts/scripts/training/main.al

on error ignore
set debug off
set authentication off
set echo queue on

:directories:
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

on error call work-dirs-error
create work directories

:call-process:
if $NODE_TYPE == master then process !local_scripts/training/generic_policies/mains/master.al
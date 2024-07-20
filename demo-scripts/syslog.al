#----------------------------------------------------------------------------------------------------------------------#
# Deploy Syslog process (for operator)
#:prepare:
#   1. Install rsyslog
#       sudo apt-get -y update
#       sudo apt -y install rsyslog
#       sudo service rsyslog start
#
#   2. Update /etc/rsyslog.conf with the following lines:
# $template remote-incoming-logs, "/var/log/remote/%HOSTNAME%.log"
# *.* ?remote-incoming-logs
# *.* action(type="omfwd" target="{{DESTINATION_IP}}" port="{DESTINATION_PORT}" protocol="tcp")
#
#   3. Restart rsyslog (service)
#       sudo service rsyslog restart
#
#:requirements:
#   1. running rsyslog
#   2. message broker
#   3. connected database
#----------------------------------------------------------------------------------------------------------------------#
# process !root_path/deployment-scripts/demo-scripts/syslog.al
on error ignore

if not !default_dbms then set default_dbms = system_logs

partition !default_dbms syslog using !partition_column by !partition_interval
schedule time=12 hours and name="Drop Partition Sync" task drop partition where dbms=!default_dbms and table=syslog and keep=3

if !broker_bind == true and !overlay_ip then set msg rule syslog_rule if ip = !overlay_ip then dbms = !default_dbms and table = syslog and syslog = true
else if !broker_bind == true and not !overlay_ip then set msg rule syslog_rule if ip = !ip then dbms = !default_dbms and table = syslog and syslog = true
else if !broker_bind == false and !overlay_ip then set msg rule syslog_rule if ip = !overlay_ip then dbms = !default_dbms and table = syslog and syslog = true
else if !broker_bind == false and not !overlay_ip then set msg rule syslog_rule if ip = !external_ip then dbms = !default_dbms and table = syslog and syslog = true

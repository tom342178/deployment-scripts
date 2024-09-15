#----------------------------------------------------------------------------------------------------------------------#
# Accept data from a local rsyslog (into operataor)
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
# process !anylog_path/deployment-scripts/demo-scripts/syslog.al
on error ignore

:partition-data:
on error goto partition-data-err
partition !default_dbms syslog using timestamp by 12 hours
schedule time=12 hours and name="Drop Partition Sync" task drop partition where dbms=!default_dbms and table=syslog and keep=3

:connect-network:
on error ignore
conn_info = get connections where format=json
is_msg_broker  = from !conn_info bring [Messaging][external]
if !is_msg_broker  == 'Not declared' then
do on error goto broker-networking-error
<do run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!!overlay_ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>

:set-syslog:
on error goto set-syslog-error
<set msg rule syslog_rule if
   ip = !ip
then
   dbms = !default_dbms  and
   table = syslog and
   syslog = true>

:end-script:
end script

:terminate-scripts:
exit scripts

:partition-data-err:
print "Error: Failed to set partitioning for default database"
goto terminate-scripts

:broker-networking-error:
print "Error: Failed to connect to Message Broker with IP address - will continue deployment without Message Broker"
do goto terminate-scripts

:set-syslog-error:
print "Error: Filed to declare message rule for data to be accepted"
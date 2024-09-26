#-----------------------------------------------------------------------------------------------------------------------
# run syslog process for operator 2
#-----------------------------------------------------------------------------------------------------------------------
on error ignore

process !anylog_path/deployment-scripts/demo-scripts/syslog.al

on error call syslog-error

syslog_ip = 45.79.18.179
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.105.86.168
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.104.180.110
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.105.13.202
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.105.60.50
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.233.107.121
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

syslog_ip = 172.105.112.207
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=!default_dbms and table=syslog and syslog=true

:end-script:
end script

:syslog-error:
echo failed to syslog for node !syslog_ip
return

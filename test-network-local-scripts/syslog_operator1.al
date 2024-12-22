#-----------------------------------------------------------------------------------------------------------------------
# run syslog process for operator 1
#-----------------------------------------------------------------------------------------------------------------------
on error ignore

process !anylog_path/deployment-scripts/demo-scripts/syslog.al

on error call syslog-error

syslog_ip = 10.10.1.10
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.201
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.212
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.214
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.216
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.206
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.203
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.32
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

:end-script:
end script

:syslog-error:
echo failed to syslog for node !syslog_ip
return

#-----------------------------------------------------------------------------------------------------------------------
# run syslog process for operator 2
#-----------------------------------------------------------------------------------------------------------------------
on error ignore

process !anylog_path/deployment-scripts/demo-scripts/syslog.al

on error call syslog-error

syslog_ip = 10.10.1.31
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.211
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.213
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.215
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.202
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.205
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

syslog_ip = 10.10.1.204
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

# syslog_ip = 10.10.1.33
# rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
# set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true

:end-script:
end script

:syslog-error:
echo failed to syslog for node !syslog_ip
return

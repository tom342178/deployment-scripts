#-----------------------------------------------------------------------------------------------------------------------
# run syslog process for operator 1
#-----------------------------------------------------------------------------------------------------------------------
on error ignore

process !anylog_path/deployment-scripts/demo-scripts/syslog.al

on error call syslog-error

syslog_ip = 45.79.74.39
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 23.239.12.151
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 172.236.61.154
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 23.92.28.183
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 139.162.56.87
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 35.208.73.148
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring.first [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 178.79.154.209
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 172.105.6.90
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

syslog_ip = 50.116.4.251
rule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]
set msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and syslog=true and extend = ip

:end-script:
end script

:syslog-error:
echo failed to syslog for node !syslog_ip
return

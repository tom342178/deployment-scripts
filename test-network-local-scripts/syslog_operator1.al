rule_name = blockchain get (master, query, publisher,  operator) where ip = 45.79.74.39 bring [*][name]
set msg rule !rule_name if ip=45.79.74.39  then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 23.239.12.151 bring [*][name]
set msg rule !rule_name if ip=23.239.12.151 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 172.236.61.154 bring [*][name]
set msg rule !rule_name if ip=172.236.61.154 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 23.92.28.183 bring [*][name]
set msg rule !rule_name if ip=23.92.28.183 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 139.162.56.87 bring [*][name]
set msg rule !rule_name if ip=139.162.56.87 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 35.208.73.148 bring [*][name]
set msg rule !rule_name if ip=35.208.73.148 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 178.79.154.209 bring [*][name]
set msg rule !rule_name if ip=178.79.154.209 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 172.105.6.90 bring [*][name]
set msg rule !rule_name if ip=172.105.6.90 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 50.116.4.251 bring [*][name]
set msg rule !rule_name if ip=50.116.4.251 then dbms=!default_dbms and table=syslog and syslog=true

rule_name = blockchain get (master, query, publisher,  operator) where ip = 69.164.203.68 bring [*][name]
set msg rule !rule_name if ip=69.164.203.68 then dbms=!default_dbms and table=syslog and syslog=true

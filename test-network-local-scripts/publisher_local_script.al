#-----------------------------------------------------------------------------------------------------------------------
# Local script for AnyLog publisher
# --> accept data via ping / percentagecpu sensor
# --> data distribution
# --> connect database for gRPC (this is a bug)
# --> start gRPC
# --> data distribution
#-----------------------------------------------------------------------------------------------------------------------
# process $ANYLOG_PATH/deployment-scripts/test-network-local-scripts/publisher_local_script.al

process $ANYLOG_PATH/deployment-scripts/demo-scripts/data_generator_ping_percentagecup_sensor.al
<set data distribution where dbms=litsanleandro and table=ping_sensor and
   dest=139.162.164.95:32148 and
   dest=172.105.13.202:32148 and
   dest=172.232.61.181:32148
>
<set data distribution where dbms=litsanleandro and table=percentagecpu_sensor and
   dest=172.105.219.25:32148 and
   dest=172.105.112.207:32148 and
   dest=50.116.61.153:32148
>

connect dbms kubearmor where type=sqlite and memory=true
process $ANYLOG_PATH/deployment-scripts/grpc/kubearmor/deploy_kubearmor_system.al
<set data distribution where
    dbms=kubearmor and
    table=* and
    dest=69.164.203.68:32148 and
    dest=172.105.6.90:32148 and
    dest=172.105.60.50:32148>


       python3 ~/Sample-Data-Generator/data_generator.py  ping 35.208.73.148:32250 mqtt \
           --batch-size 10 \
           --total-rows 10 \
           --topic ping-percentage \
           --db-name litsanleandro \
           --sleep 0
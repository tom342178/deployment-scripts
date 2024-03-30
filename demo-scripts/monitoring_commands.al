#-----------------------------------------------------------------------------------------------------------------------
# Sample commands used to get node insight
#-----------------------------------------------------------------------------------------------------------------------

# get node stats
get stats where service=operator and topic=summary and format=json

# get node name
get node name

# disk space
get disk percentage .

# cpu percent
get node info cpu_percent

# packets received
get node info net_io_counters packets_recv

# packets sent
get node info net_io_counters packets_sent

# number of network errors in
get node info net_io_counters errin

# number of network errors outu
get node info net_io_counters errout
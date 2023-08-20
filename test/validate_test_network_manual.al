#-----------------------------------------------------------------------------------------------------------------------
# The following tests the demo network deployed by users as part of their training. It is up to the user to manually
# validate the results are as expected.
# Based on: https://github.com/AnyLog-co/documentation/blob/master/training/Session%20II%20(Deployment).md#validating-the-setup-of-the-nodes-in-the-network
# :process:
#   1. View that all nodes are registered
#       Policy   Name              Ip             External_ip    Port  Rest_port
#       --------|-----------------|--------------|--------------|-----|---------|
#       operator|anylog-operator_1| 198.74.50.131| 198.74.50.131|32148|    32149|
#       query   |anylog-query     | 198.74.50.131| 198.74.50.131|32348|    32349|
#       master  |anylog-master    | 198.74.50.131| 198.74.50.131|32048|    32049|
#       operator|anylog-operator_2|178.79.143.174|178.79.143.174|32148|    32149|
#   2. Validate the cluster setup
#       Name              Cluster
#       -----------------|--------------------------------|
#       anylog-operator_1|497425abfbda8696558a715879ab8e4d|
#       anylog-operator_2|4c87fe80fada01e8260c83db82bf0a7c|
#   3. Test nodes are accessible
#       Address              Node Type Node Name         Status
#       --------------------|---------|-----------------|------|
#       198.74.50.131:32148 |operator |anylog-operator_1|  V   |
#       198.74.50.131:32348 |query    |anylog-query     |  V   |
#       198.74.50.131:32048 |master   |anylog-master    |  V   |
#       178.79.143.174:32148|operator |anylog-operator_2|  V   |
#-----------------------------------------------------------------------------------------------------------------------
# process !test_dir/validate_test_network_manual.al

on error ignore
:view-policies:
blockchain get (master, query, operator) bring.table [*] [*][name] [*][ip] [*][external_ip] [*][port] [*][rest_port]

:cluster-setup:
blockchain get operator bring.table [operator][name] [operator][cluster]

:test-network:
test network

:end-script:
end script
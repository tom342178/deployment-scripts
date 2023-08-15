#-----------------------------------------------------------------------------------------------------------------------
# The following tests the demo network deployed by users as part of their training
# :process:
#   1. check if master exists
#   2. check if query exists
#   3. check number of unique clusters
#   4. validate the two clusters do not share a name
#   5. check number of unique operators
#   6. validate the two operators do not share a name
#   7. execute `test network` to validate
#-----------------------------------------------------------------------------------------------------------------------
# process !test_dir/validate_test_network.al

on error ignore
:is-master:
is_master = blockchain get master
if not !is_master then
do print Failed to locate master node in the blockchain. Validate the LEDGER_CONN information and that the node is running
do goto end-script
else print master - found

:is-query:
is_query = blockchain get query
if not !is_query then
do print Failed to locate query node in the blockchain. Validate the node is up and running and is part of the network
else print query - found

:check-cluster:
cluster_count = blockchain get cluster bring.unique.count [*][name]
cluster1 = blockchain get cluster bring.unique.first [*][name]
cluster2 = blockchain get cluster bring.unique.last [*][name]

# check number of unique clusters
if cluster_count != 2 then
do print Found !cluster_count clusters. Expected 2 clusters
do goto end-script

# validate the two clusters aren't using the same name
if !cluster1 == !cluster2 then
do print cluster 1 and 2 share the same name, whereas each cluster should have its own name
do goto end-script
else print 2 unique clusters - found

:check-operator:
operator_count = blockchain get operator bring.unique.count [*][name]
operator1 = blockchain get operator bring.unique.first [*][name]
operator2 = blockchain get operator bring.unique.last [*][name]

# check number of unique operators
if operator_count != 2 then
do print Found !operator_count operators. Expected 2 operators
do goto end-script

# validate the two operators are not using the same name
if !operator1 == !operator2 then
do print operator 1 and 2 share the same name, whereas each operator should have its own name
do goto end-script
else print 2 unique operators - found

:test-network:
# the following step shows which nodes are part of the network, in the blockchain and whether they're accessible
test network


:end-script:
end script
# Deployment Scripts Scripts 

The following demonstrates the default deployment scripts provided as part of the Open Source deployment of EdgeLake. 

* [demo-scripts](demo-scripts) - sample commands that can be used by users
  * manual connection of network configurations
  * `run mqtt client` with hardcoded timestamp-value process - used as part of the deployment 
  * `run mqtt client` wih a policy as opposed to being hardcoded 
  * `run mqtt client` with a policy relating to blobs
  * how to connect postgres and mongo to databases
  * basic monitoring commends
  * how to deploy syslog (maybe set to enterprise)
  
* [grpc](grpc) - connecting and running gRPC client against KubeArmor

* [node-deployment](node-deployment) - deployment process for _Master_, _Operator_ and _Query_ 


## Deployment 
Based on the _training_ deployment, I created a [docker-compose deployment](docker-compose) for an open-source version of AnyLog / EdgeLake. 

* Master Configs 
```dotenv
#--- General ---
# AnyLog License Key
LICENSE_KEY=7d6a0136fa2722022431c8ca40c194f725d3a989dcec7ef9ddfeccca83cadf05776f6ef86c7f7e3cbb2b5283e7000a1e37cec998648036e069a24ff7a9c6de70e6472d9a7dc9cf8fb8a005e98e0e212b8402d4fb185f319cf9c75d20daee373b47edd4d86d6c9698dd56e96d848e952ad8ac6d39251370e445f11ea651aab6fe{'company':'Ori','expiration':'2024-07-12','type':'beta'}
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=master
# Name of the AnyLog instance
NODE_NAME=anylog-master
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32048
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32049
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=false

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false
```

* Operator Configs
```dotenv
#--- General ---
# AnyLog License Key
LICENSE_KEY=4df552a98c6d7dbb178e828fd6947b1f3fee9911e03f37fe2106160465d9edba9eb34ca5b0c6b28a2e036dd5ed4c1590d9ae74a099ff1208775e3f3de67e571058a0a2b816e7fc45e06f33cf250851ebbce80e8b60dab00da5c425941637e636285e6883ba299d7ac810411197e09e857ba906ef39ef2cd40910f019a3c44acf2023-12-01bGuest
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=operator
# Name of the AnyLog instance
NODE_NAME=anylog-operator
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32148
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32149
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=32150
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
BROKER_BIND=false

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

#--- Operator ---
# Owner of the cluster
CLUSTER_NAME=new-company-cluster1
# Logical database name
DEFAULT_DBMS=new_company

#--- MQTT ---
# Whether to enable the default MQTT process
ENABLE_MQTT=false

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false
```

* Query 
```dotenv
#--- General ---
# AnyLog License Key
LICENSE_KEY=4df552a98c6d7dbb178e828fd6947b1f3fee9911e03f37fe2106160465d9edba9eb34ca5b0c6b28a2e036dd5ed4c1590d9ae74a099ff1208775e3f3de67e571058a0a2b816e7fc45e06f33cf250851ebbce80e8b60dab00da5c425941637e636285e6883ba299d7ac810411197e09e857ba906ef39ef2cd40910f019a3c44acf2023-12-01bGuest
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=query
# Name of the AnyLog instance
NODE_NAME=anylog-query
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32348
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32349
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=false

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false
```

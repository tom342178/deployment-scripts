# Deployment Scripts Scripts 

The following demonstrates the default deployment scripts provided as part of the Open Source deployment of EdgeLake. 

* [demo-scripts](demo-scripts) - sample commands that can be used by users
  * manual connection of network configurations
  * `run mqtt client` with hardcoded timestamp-value process - used as part of the deployment 
  * `run mqtt client` wih a policy as opposed to being hardcoded 
  * `run mqtt client` with a policy relating to blobs
  * how to connect postgres and mongo to databases
  * basic monitoring commmands
  * how to deploy syslog (maybe set to enterprise)
  
* [grpc](grpc) - connecting and running gRPC client against KubeArmor

* [node-deployment](node-deployment) - deployment process for _Master_, _Operator_ and _Query_ 

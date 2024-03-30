# Deployment Scripts 

The following demonstrates the default deployment scripts provided as part AnyLog. 

* [node-deployment](node-deployment) - deployment process for _Master_, _Operator_ and _Query_

* [grpc](grpc) - connecting and running gRPC client against KubeArmor and accept data associated with _alerts_, _logs_ and _messages_ 

* [demo-scripts](demo-scripts) - sample commands that can be used by users
  * manual connection of network configurations
  * Examples for receiving data into AnyLog via a message client (_MQTT_ & _REST-POST_) or via _Kafka_   
  * how to connect postgres and mongo to databases
  * basic monitoring commends
  * how to deploy syslog
  * Setting a message client to accept data from [_FLEDGE_](https://lfedge.org/projects/fledge/)

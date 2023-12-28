# gRPC 
 
Originally developed by (G)oogle, (R)emote (P)rocedure (C)alls (_gRPC_) is the ability to call a method on a server
application on a different machine as if it were a local object. _gRPC_ can use protocol buffers as both its Interface 
Definition Language (_IDL_) and as its underlying message interchange format. 

**What is this protocol used for**: 
* **Microservices Communication**: Communication between services -- Each microservice can expose a gRPC service, and 
other microservices can communicate with it using generated client code.
* **Distributed Systems**: facilitates communication between different components of a distributed system
* **Internet of Things**: Bidirectional communication between central server and/or other devices 

**How it works**: 
Based on my understanding, the service (sporadically) sends data to the client as it comes it. The catch is that both 
_server_ and _client_ need to have a shared `pb2.py`  files that are based on proto config file. 

In my example, the proto config file is simply returning coming in. While the sever & client are (de)serializing lists
of JSON data every 10 to 30 seconds (based on the server). 

The main issue I found is the server and client need to have a shared [protocol file](dummy.proto), and corresponding 
python filed generated based on the protocol file. 

## Links
* [Real Python](https://realpython.com/python-microservices-grpc/)
* [Official Documentation](https://grpc.io/docs/what-is-grpc/introduction/#overview)


## Dummy Code 
1. Install [grpcio-tools](https://pypi.org/project/grpcio-tools/)
```shell
python3 -m pip install --upgrade grpcio-tools
```

2. Create [protocol buffer file](dummy.proto)

3. Compile file - needs to be in _AnyLog-Network/dummy_source_code/gRPC_
```shell
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dummy.proto
```

4. Run _[Server](server.py)_
```shell
python3  server.py --port 32150
```

5. Run _[Client](client.py)_
```shell
python3 client.py --conn 127.0.0.1:32150 
```

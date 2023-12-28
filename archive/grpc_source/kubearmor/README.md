# KubeArmor 

* [kubernetes_api.py](kubernetes_api.py) - Connect to kubernetes
* [port_forwarding.py](port_forwarding.py) - generic doe for port-forwarding 
* [client.py](client.py) - main

*  [vm.proto](vm.proto) - proto file
   * [vm_pb2.py](vm_pb2.py)
   * [vm_pb2_grpc.py](vm_pb2_grpc.py)

```shell
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. vm.proto
```

**Issues**: I believe connection is working properly, but I do not see the data coming in. My guess is that something in the way I call the _protocol_ processes in [client.py](client.py) is causing the issue


## How the Code Works
1. User defines the following information
   * kubernetes service port 
   * application label 
   * target service name
2. Using Kubernetes API, extract
   * pod name 
   * namespace 
3. Generate a forwarding port
4. Create channel and stab - we currently want to focus on "topic" `info`
5. Create a port-forwarding service
   * `local_port` - forwarding port 
   * `remote_host` - machine IP (tested only with localhost)
   * `remote_port` - kubernetes service port 
6. In a thread start port forwarding 
7. wait for data to come 

**Points 1 and 2 are based on the following table** 
```shell
orishadmon@Oris-Mac-mini kubearmor % kubectl get all -n kubearmor  
NAME                                        READY   STATUS    RESTARTS   AGE
pod/kubearmor-controller-569bb7795f-87mfg   2/2     Running   0          2d1h
pod/kubearmor-none-docker-d4651-52qgx       1/1     Running   0          2d1h
pod/kubearmor-operator-6f674dc9df-ds2q2     1/1     Running   0          2d1h
pod/kubearmor-relay-848df88d96-z6c4h        1/1     Running   0          2d1h

NAME                                           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)     AGE
service/kubearmor                              ClusterIP   10.101.183.68    <none>        32767/TCP   2d1h
service/kubearmor-controller-metrics-service   ClusterIP   10.100.103.220   <none>        8443/TCP    2d1h
service/kubearmor-controller-webhook-service   ClusterIP   10.101.46.39     <none>        443/TCP     2d1h

NAME                                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                                                                                                                            AGE
daemonset.apps/kubearmor-none-docker-d4651   1         1         1       1            1           kubearmor.io/btf=yes,kubearmor.io/enforcer=none,kubearmor.io/runtime=docker,kubearmor.io/socket=run_docker.sock,kubernetes.io/os=linux   2d1h

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kubearmor-controller   1/1     1            1           2d1h
deployment.apps/kubearmor-operator     1/1     1            1           2d1h
deployment.apps/kubearmor-relay        1/1     1            1           2d1h

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/kubearmor-controller-569bb7795f   1         1         1       2d1h
replicaset.apps/kubearmor-controller-79cd4bbd84   0         0         0       2d1h
replicaset.apps/kubearmor-operator-6f674dc9df     1         1         1       2d1h
replicaset.apps/kubearmor-relay-848df88d96        1         1         1       2d1h

```

  




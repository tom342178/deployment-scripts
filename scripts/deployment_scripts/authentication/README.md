# Authentication

The following directions are based on [Securing the Network](https://github.com/AnyLog-co/documentation/blob/master/examples/Secure%20Network.md) 
document, and are specifically for certificate-based authentication.
 
Certificate based authentication, can be set for a _node_ or _user_. In addition, there should be a _root_ account that's
responsible for managing access for all other members. 

**Disclaimer**: We do not recommend setting up the `root` account on the master node

## Root Authentication & Preset Permissions
Root user grants permissions to members (nodes and users) - this should be done only on a single AnyLog instance.

1. [AnyLog-Network/scripts/deployment_scripts/authentication/set_params.al](set_params.al)
presets the configurations values used to configure certificate based authentication. Directions for updating configuration 
values in [Docker](https://github.com/AnyLog-co/documentation/blob/master/deployments/Docker/docker_volumes.md) | [Kubernetes](https://github.com/AnyLog-co/documentation/blob/master/deployments/Kubernetes/volumes.md).

**Relevant Params for creating a _root_ user**: 
* root_name 
* root_password 

```anylog
process !local_scripts/deployment_scripts/authentication/set_params.al 
``` 

2. Generate keys for the Root User - if keys already exists, the script stores the private key as a
variable called `!private_key`.
```anylog
process !local_scripts/deployment_scripts/authentication/root_keys.al
```

3. Create root user policy & store in blockchain.  
```anylog
process !local_scripts/deployment_scripts/authentication/declare_root_member.al
```

At this point the node which declared the has the keys `root` can be used to declare other member in the network, as well
as their permissions. We recommend having a [node member](#declare-non-root-member) for the node as well.

## Declare non-Root Member
Except for `root` member policy, all other members must be associated with a subset of permissions of what their respective 
keys can and cannot do. The default scripts provide examples for permissions with [no restrictions](no_restrictions_permissions.al) 
and with [limited permissions](limited_permissions.al). The limited permissions allows commands such as: _get_, _sql_ and _blockchain_.

1. Declare no restrictions permissions policy 
```anylog
process !local_scripts/deployment_scripts/authentication/no_restrictions_permissions.al
```

2. Declare limited permissions policy
```anylog
process !local_scripts/deployment_scripts/authentication/limited_permissions.al 
```

### Node Authentication
The node authentication requires access to **both** the new AnyLog node (_new node_), as-well-as a node with permissions that allows 
adding a new AnyLog instance to the network (_root node_). If you do not have access to such a node, please work with your administrator
to connect your node to the network.

1. [AnyLog-Network/scripts/deployment_scripts/authentication/set_params.al](set_params.al)
presets the configurations values used to configure certificate based authentication; this step needs to be done on **both**
the _root node_, as-well-as the _new node_ being added to the network. Directions for updating configuration 
values in [Docker](https://github.com/AnyLog-co/documentation/blob/master/deployments/Docker/docker_volumes.md) | [Kubernetes](https://github.com/AnyLog-co/documentation/blob/master/deployments/Kubernetes/volumes.md).

**Relevant Params on New Node**: 
* `node_password` - node password for when creating node_keys -- used for both private and local password in enable_authentication.al


**Relevant Params on Root Node**: 
* `remote_node_conn` - IP:PORT information for _new node_ that"ll be added to network 
* `remote_node_name` - set the name for the _new node_ you want to add to the network
* `remote_node_company` - set the company associated with the _new node_

```anylog
process !local_scripts/deployment_scripts/authentication/set_params.al 
```

2. On the _new node_ create a private and public key - if keys already exists, the script stores the private key as a
variable called `!private_key_node`.
```anylog
process !local_scripts/deployment_scripts/authentication/node_keys.al
```

3. On the _root node_ declare a member policy that"ll be associated with the _new node_
```anylog
process !local_scripts/deployment_scripts/authentication/declare_node_member.al
```

4. Once a member policy is declared for a node, the _root node_ needs to give this member permissions. The scripts provided
currently give (new) node members full access. However, administrators may choose to set different permissions for different
nodes. Directions for updating configuration values in [Docker](https://github.com/AnyLog-co/documentation/blob/master/deployments/Docker/docker_volumes.md) | [Kubernetes](https://github.com/AnyLog-co/documentation/blob/master/deployments/Kubernetes/volumes.md).
```anylog
process !local_scripts/deployment_scripts/authentication/assign_node_privileges.al
```

5. Once a member policy (and it's permissions) are declared, then the _new node_ can enable authentication. The script 
also configures [password security](../../authentication.md#passwords) for the private key using `node_password` as the 
default password value. 
```anylog
process !local_scripts/deployment_scripts/authentication/enable_authentication.al 
```
At this point the _new node_, has the correct privileges to communicate with the network, and act as is expected of it.
If the _new node_ is configured as _REST_, then users can **either** deploy the process(es) for the desired node type
**or** execute `blockchain sync` in view its privileges, and access other nodes in the network. 

```anylog 
# blockchain sync
run blockchain sync where source=!blockchain_source and time=!sync_time and dest=!blockchain_destination and connection=!ledger_conn

# deploy a desired node type on the node - the example is for an Operator Node 
process !local_scripts/run_scripts/start_operator.al 
```

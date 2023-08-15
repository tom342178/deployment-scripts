# Authentication & Security
The following provides a simplified explanation for securing an AnyLog node / network using the associated AnyLog
scripts.  

* [Authentication](https://github.com/AnyLog-co/documentation/blob/master/authentication.md)
* [Security](https://github.com/AnyLog-co/documentation/blob/master/examples/Secure%20Network.md)

## REST Authentication
AnyLog REST authentication configures the node to require users to specify authentication information when sending
requests via _REST_.

1. On the AnyLog node enable REST authentication
   * set local (node) password
   * enable user authentication 
   * create user 
```anylog
process !local_scripts/deployment_scripts/authentication/basic_rest_authentication.al
```

2. Declare variable consisting of username and password with [base64](https://linux.die.net/man/1/base64) encoding. 
Make sure the username and password match the credentials used wheb declaring `id user` command.   
```shell
AUTH=`echo -ne "$USERNAME:$PASSWORD" | base64 --wrap 0`
```

3. Execute cURL command 
```shell
curl -X GET 127.0.0.1:32049 -H "command: get status" -H "User-Agent: AnyLog/1.23" -H "Authentication: ${AUTH}"
```
Reminder, there is no need for _Authentication_ header if REST authentication is disabled  


## Security 

The following steps should be done a node that'll act as a "root" account within the network

1. On an AnyLog node, declare root user. _Root_ is the only member that can grant permissions to other 
users and/or nodes.
   * Generate keys for the Root User
   * Declare root user policy
```anylog
process !local_scripts/deployment_scripts/authentication/member_root_user.al
```

2. Declare permissions to be used be used by users and / or node within the network
   * [permissions_no_restrictions.al](permissions_no_restrictions.al) - access to all commands and databases 
   * [permissions_limited_restrictions.al](permissions_limited_restrictions.al) - access to all commands and databases, 
   except `drop` command 
   * [permissions_master.al](permissions_master.al) - access to commands, but only access to the blockchain logical database
   * [permissions_operator.al](permissions_operator.al) - access to commands, but only access to the _default_ operator 
   database and `almgm` logical database
```anylog
process !local_scripts/deployment_scripts/authentication/permissions_no_restrictions.al
process !local_scripts/deployment_scripts/authentication/permissions_limited_restrictions.al
process !local_scripts/deployment_scripts/authentication/permissions_master.al
process !local_scripts/deployment_scripts/authentication/permissions_operator.al
```
   
The following steps should be done on the same AnyLog nodes the user wants the private / public key to reside

3a. On each AnyLog node, declare an associated member policy
   * Generate keys for the node
   * Declare member node policy 
```anylog
process !local_scripts/deployment_scripts/authentication/member_node.al
```

3b. Create a policy for a specific user
   * Generate keys for the user
   * Declare member user policy
```anylog
process !local_scripts/deployment_scripts/authentication/member_user.al
```

4. Once **both** _members_ and _permissions_ are define, the root user, or someone with root privileges, needs to associate
between member(s) and permission(s).
* Sample call for associating a node with a set of permissions 
```anylog
process !local_scripts/deployment_scripts/authentication/assignment_node.al
```
* Sample call for associating a user with a set of permissions
```anylog
process !local_scripts/deployment_scripts/authentication/assignment_user.al
```

## Communication using Keys
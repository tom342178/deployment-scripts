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



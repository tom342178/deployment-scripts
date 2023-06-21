# Deployment Scripts

## Process 
The following provides step by step explanation of how the default process works (with sample commands)
0. Everything is called from [start_node.al](run_scripts/start_node.al)
1. Based on `$ANYLOG_PATH` set the AnyLog "home" or "root" path & create directories
```anylog
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
create work directories
```
2. [set_params.al](deployment_scripts/set_params.al) - converts environment parameters into AnyLog parameters 
```anylog
hostname = get hostname
node_name = anylog-node
company_name = "New Company"
country = "Unknown"
state = "Unknown"
city = "Unknown"

if $NODE_NAME then node_name = $NODE_NAME
if $COMPANY_NAME then company_name = $COMPANY_NAME
if $LOCATION then loc = $LOCATION
if $COUNTRY then country = $COUNTRY
if $STATE then state = $STATE
if $CITY then city = $CITY
...
```

3. [network_configs.al](deployment_scripts/network_configs.al) - Setup network configurations, such as TCP and REST
```anylog
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port 
run rest server !anylog_rest_port 
```

4. [configure_dbms_operator.al](deployment_scripts/database/configure_dbms_operator.al) - Connect to relevent databases
   * Master Node requires database named `ledger`
   * Operator Node requires the local logical database + blobs database (if set)
   * Query Node requires `system_query` logical database to accept / aggregate query results 
   * Both the Operator Node and Publisher node require an anylog management database (`almgm`) which is used to keep 
   track of data taht has came in
```anylog
<connect dbms ${DB_NAME} where 
    type=${DB_TYPE} and 
    ip=${DB_IP} and 
    port=${DB_PORT} and 
    user=${DB_USER} and 
    password=${DB_PASSSWD}
>
```

5. [run_scheduler.al](deployment_scripts/run_scheduler.al) - Run the default scheduling processes 
   * Scheduler 1 
   * Blockchain sync 


6. [declare_generic_policy.al](deployment_scripts/declare_generic_policy.al) - Declare policy on blockchain 
```anylog 
<new_policy = {!policy_type: {
    "hostname": !hostname,
    "name": !node_name,
    "ip" : !external_ip,
    "local_ip": !ip,
    "company": !company_name,
    "port" : !anylog_server_port.int,
    "rest_port": !anylog_rest_port.int,
    "loc": !loc,
    "country": !country,
    "state": !state, 
    "city": !city
}}>

on error call declare-policy-error
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

7. Execute node specific configurations
   * partitions for operator node(s) 
   * Buffer threshold and streamer 
   * `run operator` || `run publisher` process 

8. Deploy local script(s), such as MQTT or some other special program


## Sample Local Scripts
* [edgex.al](sample_code/edgex.al) - provides a policy based example for _EdgeX_'s sample data generator. 
* [edgex_humidity_temp.al](../archive/fujitsu/edgex_humidity_temp.al) - provides a policy based example for _EdgeX_'s Temp/Humidity demo 
* [fledge.al](sample_code/fledge.al) - provides example code for multiple topics under the same `run mqtt client` command
accepting data from _FLEDGE_ random data generator and weather app. 
* [deeptector.al](../archive/blob_image_data_base64.al) - policy based `run mqtt client` for NTT's _Deeptector_ image analyzer 
* [car_data.al](../archive/blob_video_data_base64.al) - image / data policy based used in [Sample Data Generator](https://github.com/AnyLog-co/Sample-Data-Generator/blob/master/data_generator_file_processing.py)
* [nvidia.al](../archive/NVIDIA/log_files.al) - code used for NVIDIA POC with _Fleet Command_
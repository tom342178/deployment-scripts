# Sample Code 
The following provides different example of the `run msg client` command. 

The `run msg client` command can be used with either _REST-POST_ or an _MQTT broker_ interchangeably.

## Basic MQTT Client
Connect to an MQTT broker, provided:
- connection information to the broker
- mapping instructions from source data (_timestamp_/_value_) to the destination format

```anylog
process !local_scripts/sample_code/deploy_basic_mqtt_process.al
```

## Single MQTT client and Topic with Multiple Data Sources 
[EdgeX](edgex.al) provides an example of receiving data from multiple sources to the same _MQTT_ topic. 

The code uses policies to define mapping instructions.

Directions for downloading and sending data into AnyLog can be found in our [EdgeX](https://github.com/AnyLog-co/lfedge-code/tree/main/edgex)
repository. 

```anylog
process !local_scripts/sample_code/edgex.al
```

## Single MQTT client with Multiple Topics
[FLEDGE](../../demo_scripts/fledge.al) provides an example of receiving data from multiple topics against the same _REST_ connection.

**Directions**: 
1. Install [FLEDGE](https://fledge-iot.readthedocs.io/en/latest/quick_start/installing.html)

2. Extend _FLEDGE_ to include [AnyLog connector](https://github.com/AnyLog-co/lfedge-code/tree/main/fledge)

3. On the AnyLog side run [FLEDGE](../../demo_scripts/fledge.al)
```anylog
process !local_scripts/sample_code/fledge.al 
```

## Image & Video Processing
Blob data is stored using policy-based instructions for `mqtt client`. The [Sample Data Generator](https://github.com/AnyLog-co/Sample-Data-Generator)
provides directions for inserting blobs into AnyLog. 

**Example 1**: Image Blobs
The images are based on data provided by a third party, and include coordinates on an error on the picture. Data is 
expected to come-in via _REST POST_. 
```anylog
process !local_scripts/sample_code/blob_image_data.al 
```

**Example 2**: Video Processing 
The videos are of traffic data. The sample data generator associates random values with videos. Data is expected to 
come-in via a local _MQTT broker_. 
```anylog
process !local_scripts/sample_code/blob_video_data.al 
```


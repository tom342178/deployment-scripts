# Testing 

* [Test Suite](https://github.com/AnyLog-co/documentation/blob/master/test%20suites.md)

## How to Run
1. Declare a test database on the operator node(s)
```anylog 
create database test where type=[sqlite | psql] [and host = 127.0.0.1 and port=5432 and user=admin and password=passwd] 
```

2. Create A new cluster(s) for test database 
```anylog

```

3. Initiate a _Publisher_ node if doesn't exist - [directions for deploying node](https://github.com/AnyLog-co/documentation/blob/master/deployments/deploying_node.md)

4. On the _Publisher_ node execute data insertion - Publisher node will distribute the data among the operator nodes 
```anylog
AL > process !test_dir/data/copy_files.al 
```

5. Execute tests

## Test Breakdown
```editorconfig
$HOME/AnyLog-Network/data/test/altests/
├── anylog_functions <-- period & increment testing 
│   ├── percentagecpu_sensor_day_increments.out
│   ├── percentagecpu_sensor_hour_increments.out
│   ├── percentagecpu_sensor_hour_increments_group_string.out
│   ├── percentagecpu_sensor_hour_increments_group_uuid.out
│   ├── percentagecpu_sensor_month_increments.out
│   ├── percentagecpu_sensor_week_increments.out
│   ├── ping_sensor_hardcoded_period.out
│   ├── ping_sensor_hardcoded_period_group_string.out
│   ├── ping_sensor_hardcoded_period_group_uuid.out
│   ├── ping_sensor_hardcoded_period_group_where_uuid.out
│   └── ping_sensor_period_now.out
├── demo_queries <-- Queries based on the demo   
│   ├── demo_image.out
│   ├── demo_image_europe.out
│   ├── demo_query2.out
│   ├── demo_video_period.out
│   ├── demo_video_timestamp_europe.out
│   ├── demo_video_timestamp_no_timezone.out
│   └── demo_video_timestamp_timezone.out
└── validate_data <-- basic aggregate queries 
    ├── image_summary.out
    ├── image_summary_where_int.out
    ├── image_summary_where_int_string.out
    ├── image_summary_where_string.out
    ├── percentagecpu_sensor_summary.out
    ├── percentagecpu_sensor_summary_group_string.out
    ├── percentagecpu_sensor_summary_group_uuid.out
    ├── percentagecpu_sensor_summary_where_string.out
    ├── percentagecpu_sensor_summary_where_timestamp.out
    ├── percentagecpu_sensor_summary_where_timestamp_string.out
    ├── percentagecpu_sensor_summary_where_timestamp_string_group_uuid.out
    ├── percentagecpu_sensor_summary_where_timestamp_uuid.out
    ├── percentagecpu_sensor_summary_where_timestamp_uuid_group_string.out
    ├── percentagecpu_sensor_summary_where_uuid.out
    ├── ping_sensor_summary.out
    ├── ping_sensor_summary_group_string.out
    ├── ping_sensor_summary_group_uuid.out
    ├── ping_sensor_summary_where_string.out
    ├── ping_sensor_summary_where_timestamp.out
    ├── ping_sensor_summary_where_timestamp_string.out
    ├── ping_sensor_summary_where_timestamp_string_group_uuid.out
    ├── ping_sensor_summary_where_timestamp_uuid.out
    ├── ping_sensor_summary_where_timestamp_uuid_group_string.out
    ├── ping_sensor_summary_where_uuid.out
    ├── video_based_on_file_within_range.out
    ├── video_based_on_file_within_range_and_params.out
    └── video_summary.out
```
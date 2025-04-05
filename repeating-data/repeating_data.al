#---------------------------------------------------------------------------------------------------------------------#
# The following demonstrates catching repeating values for data coming in.
#---------------------------------------------------------------------------------------------------------------------#
# process !anylog_path/deployment-scripts/repeating-data/repeating_data.al

if not !default_dbms then default_dbms = new_company
table_name = rand_int3
aggregations_interval_time = 1 minute
num_intervals = 10
time_column = insert_timestamp
value_column = value
min_threshold = 0
max_threshold = 10

<set aggregations where
    dbms=!default_dbms and
    table=!table_name and
    intervals = !num_intervals and
    time = !aggregations_interval_time and
    time_column = !time_column and
    value_column = !value_column
>


<set aggregations threshold where
    dbms = !default_dbms and
    table = !table_name and
    min = !min_threshold and
    max = !max_threshold
>

# Only insert min and max from every log processed

set aggregations script where dbms = !default_dbms and table = !table_name and script = streaming data update bounds

get aggregations where config = true

# Add Data

get aggregations
#-----------------------------------------------------------------------------------------------------------------------
# Table blockchain table policy for monitoring
#   -> create table policy
#   -> if operator then: connect dbms (monitoring), create table, set partitioning
# :sample table:

# CREATE TABLE IF NOT EXISTS node_insight(
#   row_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   tsd_name CHAR(3),
#   tsd_id INT,
#   node_name varchar,
#   status varchar,
#   operational_time TIME NOT NULL DEFAULT '00:00:00',
#   processing_time TIME NOT NULL DEFAULT '00:00:00',
#   elapsed_time TIME NOT NULL DEFAULT '00:00:00',
#   new_rows INT,
#   total_rows INT,
#   new_errors INT,
#   total_errors INT,
#   avg_rows_sec FLOAT,
#   timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   free_space_percent FLOAT,
#   cpu_percent FLOAT,
#   packets_recv INT,
#   packets_sent INT,
#   network_error INT
# );
# CREATE INDEX node_insight_timestamp_index ON node_insight(timestamp);
# CREATE INDEX node_insight_tsd_index ON node_insight(tsd_name, tsd_id);
# CREATE INDEX node_insight_insert_timestamp_index ON node_insight(insert_timestamp);
# CREATE INDEX node_insight_node_name_index ON node_insight(node_name);
#-----------------------------------------------------------------------------------------------------------------------
# process !anylog_path/deployment-scripts/demo-scripts/monitoring_table_policy.al
on error ignore

set create_table = false
:check-table-policy:
is_table = blockchain get table where dbms=monitoring and name=node_insight
if !is_table then goto end-script
else if not !is_table and !create_table == true then goto declare-policy-error

:declare-policy:
<new_policy = {
    "table": {
        "dbms": "monitoring",
        "name": "node_insight",
        "create": "CREATE TABLE IF NOT EXISTS node_insight( row_id INTEGER PRIMARY KEY AUTOINCREMENT, insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, tsd_name CHAR(3), tsd_id INT, node_name varchar, status varchar, operational_time TIME NOT NULL DEFAULT '00:00:00', processing_time TIME NOT NULL DEFAULT '00:00:00', elapsed_time TIME NOT NULL DEFAULT '00:00:00', new_rows INT, total_rows INT, new_errors INT, total_errors INT, avg_rows_sec FLOAT, timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, free_space_percent FLOAT, cpu_percent FLOAT, packets_recv INT, packets_sent INT, network_error INT ); CREATE INDEX node_insight_timestamp_index ON node_insight(timestamp); CREATE INDEX node_insight_tsd_index ON node_insight(tsd_name, tsd_id); CREATE INDEX node_insight_insert_timestamp_index ON node_insight(insert_timestamp); CREATE INDEX node_insight_node_name_index ON node_insight(node_name);"
    }
}>

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
else if !error_code == 2 then goto prepare-policy-error
else if !error_code == 3 then goto declare-policy-error
set create_table = true
goto check-table-policy

:end-script:
end script

:terminate-scripts:
exit scripts

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts
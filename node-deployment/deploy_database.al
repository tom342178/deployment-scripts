#----------------------------------------------------------------------------------------------------------------
# Deploy database(s) based on node type and configuration
# -- for operator also deploy partitions if set
#----------------------------------------------------------------------------------------------------------------
# process !local_scripts/deploy_database.al

on error ignore

if !node_type == master then
do connect dbms blockchain where type=!db_type
do create table ledger where dbms=blockchain

if !node_type == operator then
do connect dbms !default_dbms where type=!db_type
do connect dbms almgm where type=!db_type
do create table tsd_info where dbms=almgm
do partition !default_dbms !table_name using !partition_column by !partition_interval
do schedule time=!partition_sync and name="Drop Partitions" task drop partition where dbms=!default_dbms and table =!table_name and keep=!partition_keep
<do run blobs archiver where
    dbms=!blobs_dbms and
    folder=!blobs_folder and
    compress=!blobs_compress and
    reuse_blobs=!blobs_reuse
>

if !deploy_system_query == true then connect dbms system_query where type=!db_type and memory=!memory

:end-script:
end script
#----------------------------------------------------------------------------------------------------------------------#
# Manually set env params if fails to set home path
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/set_paths.al
if !debug_mode == true then
do print "Manually set file paths to be used
do set debug on

on error ignore
if !is_edgelake == true then goto set-edgelake

:set-anylog:
pem_dir =!anylog_path/AnyLog-Network/data/pem
prep_dir=!anylog_path/AnyLog-Network/data/prep 
tmp_dir =!anylog_path/AnyLog-Network/data/tmp
watch_dir =!anylog_path/AnyLog-Network/data/watch
dbms_dir=!anylog_path/AnyLog-Network/data/dbms 
distr_dir =!anylog_path/AnyLog-Network/data/distr
err_dir =!anylog_path/AnyLog-Network/data/error
archive_dir =!anylog_path/AnyLog-Network/data/archive
bkup_dir=!anylog_path/AnyLog-Network/data/bkup 
blobs_dir =!anylog_path/AnyLog-Network/data/blobs
blockchain_dir=!anylog_path/AnyLog-Network/blockchain
blockchain_file =!anylog_path/AnyLog-Network/blockchain/blockchain.json
blockchain_new=!anylog_path/AnyLog-Network/blockchain/blockchain.new 
blockchain_sql=!anylog_path/AnyLog-Network/blockchain/blockchain.sql 
bwatch_dir=!anylog_path/AnyLog-Network/data/bwatch
goto create-paths

:set-edgelake:
pem_dir =!anylog_path/EdgeLake/data/pem
prep_dir=!anylog_path/EdgeLake/data/prep
tmp_dir =!anylog_path/EdgeLake/data/tmp
watch_dir =!anylog_path/EdgeLake/data/watch
dbms_dir=!anylog_path/EdgeLake/data/dbms
distr_dir =!anylog_path/EdgeLake/data/distr
err_dir =!anylog_path/EdgeLake/data/error
archive_dir =!anylog_path/EdgeLake/data/archive
bkup_dir=!anylog_path/EdgeLake/data/bkup
blobs_dir =!anylog_path/EdgeLake/data/blobs
blockchain_dir=!anylog_path/EdgeLake/blockchain
blockchain_file =!anylog_path/EdgeLake/blockchain/blockchain.json
blockchain_new=!anylog_path/EdgeLake/blockchain/blockchain.new
blockchain_sql=!anylog_path/EdgeLake/blockchain/blockchain.sql
bwatch_dir=!anylog_path/EdgeLake/data/bwatch

:create-paths:
system mkdir -p !pem_dir
system mkdir -p !prep_dir
system mkdir -p !tmp_dir
system mkdir -p !watch_dir
system mkdir -p !dbms_dir
system mkdir -p !distr_dir
system mkdir -p !err_dir
system mkdir -p !archive_dir
system mkdir -p !bkup_dir
system mkdir -p !blobs_dir
system mkdir -p !blockchain_dir
system mkdir -p !bwatch_dir
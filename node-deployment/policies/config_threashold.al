#----------------------------------------------------------------------------------------------------------------------#
# Set buffer threshold
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/policies/config_threashold.al

:set-params:
threshold_dbms = ""
threshold_table = ""

on error goto threshold-error
if !threshold_dbms and !threshold_table then
<do set buffer threshold where
    dbms=!threshold_dbms and table=!threshold_table and
    time=!threshold_time and
    volume=!threshold_volume and
    write_immediate=!write_immediate>
if !threshold_dbms and not !threshold_table then
<do set buffer threshold where
    dbms=!threshold_dbms and
    time=!threshold_time and
    volume=!threshold_volume and
    write_immediate=!write_immediate>
if not !threshold_dbms and not !threshold_table then
<do set buffer threshold where
    time=!threshold_time and
    volume=!threshold_volume and
    write_immediate=!write_immediate>

:end-sccript:
end script

:threshold-error:
echo "Failed to set threshold"
goto end-script
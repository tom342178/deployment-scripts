:set-params:
on error ignore
if not !mqtt_log and $MQTT_LOG then set mqtt_log = $MQTT_LOG
else if not !mqtt_log then set mqtt_log = false

topic_name = opcua-datas

:mqtt-client:
on error goto mqtt-client-error
if !anylog_broker_port then
<do run mqtt client where broker=local and port=!anylog_broker_port and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.fic1_pv=(type=float and value="bring [fic1_pv]") and
    column.fic1_mv=(type=float and value="bring [fic1_sv]") and
    column.fic1_mv=(type=float and value="bring [fic1_mv]") and
    column.lic1_pv=(type=float and value="bring [lic1_pv]") and
    column.lic1_mv=(type=float and value="bring [lic1_sv]") and
    column.lic1_mv=(type=float and value="bring [lic1_mv]") and
    column.fic2_pv=(type=float and value="bring [fic2_pv]") and
    column.fic2_mv=(type=float and value="bring [fic2_sv]") and
    column.fic2_mv=(type=float and value="bring [fic2_mv]") and
    column.lic2_pv=(type=float and value="bring [lic2_pv]") and
    column.lic2_mv=(type=float and value="bring [lic2_sv]") and
    column.lic2_mv=(type=float and value="bring [lic2_mv]") and
    column.fic3_pv=(type=float and value="bring [fic3_pv]") and
    column.fic3_mv=(type=float and value="bring [fic3_sv]") and
    column.fic3_mv=(type=float and value="bring [fic3_mv]") and
    column.lic3_pv=(type=float and value="bring [lic3_pv]") and
    column.lic3_mv=(type=float and value="bring [lic3_sv]") and
    column.lic3_mv=(type=float and value="bring [lic3_mv]") and
    column.fic4_pv=(type=float and value="bring [fic4_pv]") and
    column.fic4_mv=(type=float and value="bring [fic4_sv]") and
    column.fic4_mv=(type=float and value="bring [fic4_mv]") and
    column.lic4_pv=(type=float and value="bring [lic4_pv]") and
    column.lic4_mv=(type=float and value="bring [lic4_sv]") and
    column.lic4_mv=(type=float and value="bring [lic4_mv]") and
    column.fic5_pv=(type=float and value="bring [fic2_pv]") and
    column.fic5_mv=(type=float and value="bring [fic2_sv]") and
    column.fic5_mv=(type=float and value="bring [fic2_mv]") and
    column.lic5_pv=(type=float and value="bring [lic2_pv]") and
    column.lic5_mv=(type=float and value="bring [lic2_sv]") and
    column.lic5_mv=(type=float and value="bring [lic2_mv]")
)>
<else run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
        column.fic1_pv=(type=float and value="bring [fic1_pv]") and
    column.fic1_mv=(type=float and value="bring [fic1_sv]") and
    column.fic1_mv=(type=float and value="bring [fic1_mv]") and
    column.lic1_pv=(type=float and value="bring [lic1_pv]") and
    column.lic1_mv=(type=float and value="bring [lic1_sv]") and
    column.lic1_mv=(type=float and value="bring [lic1_mv]") and
    column.fic2_pv=(type=float and value="bring [fic2_pv]") and
    column.fic2_mv=(type=float and value="bring [fic2_sv]") and
    column.fic2_mv=(type=float and value="bring [fic2_mv]") and
    column.lic2_pv=(type=float and value="bring [lic2_pv]") and
    column.lic2_mv=(type=float and value="bring [lic2_sv]") and
    column.lic2_mv=(type=float and value="bring [lic2_mv]") and
    column.fic3_pv=(type=float and value="bring [fic3_pv]") and
    column.fic3_mv=(type=float and value="bring [fic3_sv]") and
    column.fic3_mv=(type=float and value="bring [fic3_mv]") and
    column.lic3_pv=(type=float and value="bring [lic3_pv]") and
    column.lic3_mv=(type=float and value="bring [lic3_sv]") and
    column.lic3_mv=(type=float and value="bring [lic3_mv]") and
    column.fic4_pv=(type=float and value="bring [fic4_pv]") and
    column.fic4_mv=(type=float and value="bring [fic4_sv]") and
    column.fic4_mv=(type=float and value="bring [fic4_mv]") and
    column.lic4_pv=(type=float and value="bring [lic4_pv]") and
    column.lic4_mv=(type=float and value="bring [lic4_sv]") and
    column.lic4_mv=(type=float and value="bring [lic4_mv]") and
    column.fic5_pv=(type=float and value="bring [fic2_pv]") and
    column.fic5_mv=(type=float and value="bring [fic2_sv]") and
    column.fic5_mv=(type=float and value="bring [fic2_mv]") and
    column.lic5_pv=(type=float and value="bring [lic2_pv]") and
    column.lic5_mv=(type=float and value="bring [lic2_sv]") and
    column.lic5_mv=(type=float and value="bring [lic2_mv]")
)>

:end-script:
end script

:json-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:declare-policy-error:
echo "Failed to declare policy on blockchain"
return
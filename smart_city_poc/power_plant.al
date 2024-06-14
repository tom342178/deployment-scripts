#----------------------------------------------------------------------------------------------------------------------#
# Create policy for power plant
# :Expected Table:
#    CREATE TABLE IF NOT EXISTS power_plant(
#        row_id SERIAL PRIMARY KEY,
#        insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
#        tsd_name CHAR(3),
#        tsd_id INT,
#        timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
#        device char(4),
#        a_current int,
#        a_n_voltage int,
#        b_current int,
#        b_n_voltage int,
#        c_current int,
#        c_n_voltage int,
#        energy_multiplier int,
#        frequency int,
#        power_factor int,
#        reactive_power int,
#        real_power int
#    );
#    CREATE INDEX power_plant_timestamp_index ON power_plant(timestamp);
#    CREATE INDEX power_plant_tsd_index ON power_plant(tsd_name, tsd_id);
#    CREATE INDEX power_plant_insert_timestamp_index ON power_plant(insert_timestamp);',
# :Data from Dynics:
#   {
#       "timestamp": DATETIME.FUNCTION(),
#       "device": field.Name,
#       "commsstatus": recordBatch.Column(commsstatus).GetValue(0),
#       "a_current": recordBatch.Column(a_current).GetValue(0),
#       "a_n_voltage": recordBatch.Column(a_n_voltage).GetValue(0),
#       "b_current": recordBatch.Column(b_current).GetValue(0),
#       "b_n_voltage": recordBatch.Column(b_n_voltage).GetValue(0),
#       "c_current": recordBatch.Column(c_current).GetValue(0),
#       "c_n_voltage": recordBatch.Column(c_n_voltage).GetValue(0),
#       "energymultiplier": recordBatch.Column(energymultiplier).GetValue(0),
#       "frequency": recordBatch.Column(frequency).GetValue(0),
#       "powerfactor": recordBatch.Column(powerfactor).GetValue(0),
#       "reactivepower": recordBatch.Column(reactivepower).GetValue(0),
#       "realpower": recordBatch.Column(realpower).GetValue(0),
#   }
#----------------------------------------------------------------------------------------------------------------------#

:set-params:
policy_id = cos-power-plant
if not !default_dbms then default_dbms=cos
table_name = power_plant

:prepare-policy:
policy = blockchain get mapping where id = !policy_id
if !policy then goto msg-call


:create-policy:
set new_policy = ""
<new_policy = {
    "id": !policy_id,
    "dbms": !default_dbms,
    "table": !table_name,
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now(),
            "bring": "[timestamp]",
        },
        "device: {
            "type": "string",
            "bring": "device"
        },
        "comms_status": {
            "type": "bool",
            "bring": "[commsstatus]"
        },
        "a_current": {
            "type": "int",
            "bring": "[a_current]"
        },
        "a_n_voltage": {
            "type": "int",
            "bring": "[a_n_voltage]"
        },
        "b_current": {
            "type": "int",
            "bring": "[b_current]"
        },
        "b_n_voltage": {
            "type": "int",
            "bring": "[b_n_voltage]"
        },
        "c_current": {
            "type": "int",
            "bring": "[c_current]"
        },
        "c_n_voltage": {
            "type": "int",
            "bring": "[c_n_voltage]"
        },
        "energy_multiplier": {
            "type": "int",
            "bring": "[energymultiplier]"
        },
        "frequency": {
            "type": "int",
            "bring": "[frequency]"
        },
        "power_factor": {
            "type": "int",
            "bring": "[powerfactor]"
        },
        "reactive_power": {
            "type": "int",
            "bring": "[reactivepower]"
        },
        "real_power": {
            "type": "int",
            "bring": "[realpower]"
        }
    }
}>

:test-policy:
test_policy = json !new_policy test
if !test_policy == false then goto test-policy-error

:publish-policy:
process !local_scripts/policies/publish_policy.al
if !error_code == 1 then goto sign-policy-error
if !error_code == 2 then goto prepare-policy-error
if !error_code == 3 then goto declare-policy-error

:msg-call:
if !anylog_broker_port then
<do run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port and !user_name and !user_password then
<do run msg client where broker=rest and port=!anylog_rest_port and user=!user_name and password=!user_password and user-agent=anylog and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>
else if not !anylog_broker_port then
<do run msg client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
    name=!policy_id and
    policy=!policy_id
)>

:end-script:
end script

:terminate-scripts:
exit scripts

:test-policy-error:
echo "Invalid JSON format, cannot declare policy"
goto end-script

:sign-policy-error:
print "Failed to sign cluster policy"
goto terminate-scripts

:prepare-policy-error:
print "Failed to prepare member cluster policy for publishing on blockchain"
goto terminate-scripts

:declare-policy-error:
print "Failed to declare cluster policy on blockchain"
goto terminate-scripts

:policy-error:
print "Failed to publish policy for an unknown reason"
goto terminate-scripts


:msg-error:
echo "Failed to deploy MQTT process"
goto end-script

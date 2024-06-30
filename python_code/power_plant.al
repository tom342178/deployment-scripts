#-----------------------------------------------------------------------------------------------------------------------
# Case 1:
# {"BG10.CommsStatus":true,"BG11.CommsStatus":true,"BG8.CommsStatus":true,"BG9.CommsStatus":true,"CG12.CommsStatus":true,
#  "CG7.CommsStatus":true,"DG2.CommsStatus":true,"DG3.CommsStatus":true,"DG4.CommsStatus":true,"DG5.CommsStatus":true,
#  "DG6.CommsStatus":true,"BCT.CommsStatus":true,"BF1.CommsStatus":true,"BF2.CommsStatus":true,"BF3.CommsStatus":true,
#  "id":914,"Timestamp":"2024-06-30T03:27:32.1940000Z"}
# Case 2:
# {"BG10.A_Current":0,"BG10.A_N_Voltage":0,"BG10.B_Current":0,"BG10.B_N_Voltage":0,"BG10.C_Current":0,
#  "BG10.C_N_Voltage":0,"BG10.EnergyMultiplier":1,"BG10.Frequency":6000,"BG10.PowerFactor":100,"BG10.ReactivePower":0,
#  "BG10.RealPower":0,"BG11.A_Current":0,"BG11.A_N_Voltage":0,"BG11.B_Current":0,"BG11.B_N_Voltage":0,"BG11.C_Current":0,
#  ..., "Timestamp":"2024-06-30T03:27:55.8240000Z"}
# Case 3:
#  {"BCT.A_Current":81,"BCT.A_N_Voltage":732,"BCT.B_Current":80,"BCT.B_N_Voltage":735,"BCT.C_Current":85,
#   "BCT.C_N_Voltage":733,"BCT.EnergyMultiplier":1,"BCT.Frequency":6000,"BCT.PowerFactor":96,"BCT.ReactivePower":532,
#   "BCT.RealPower":1719,"CBT.A_Current":81,"CBT.A_N_Voltage":733,"CBT.B_Current":81,"CBT.B_N_Voltage":736,
#   "CBT.C_Current":85,"CBT.C_N_Voltage":735,"CBT.EnergyMultiplier":1,"CBT.Frequency":6000,"CBT.PowerFactor":96,
#   ..., "Timestamp":"2024-06-30T05:35:58.5460000Z"}


default_dbms = power_plant
policy_id_commsstatus = smart-city-pp-commsstatus
policy_id_other = smart-city-pp-other
policy_id = smart-city-pc

:prepare-policy:
<new_policy  = {
    "transform": {
        "id": !policy_id_commsstatus,
        "name" : "Smart City PP PLC mapper - commsstatus",
        "dbms": !default_dbms,
        "re_match" : "([^.]*)\\.(.*)",
        "table": "commsstatus",
        "column": "re.group(1)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[Timestamp]",
                "default" : "now()"
            }
        }
    }
}>


<new_policy  = {
    "transform": {
        "id": !policy_id,
        "name" : "Smart Ctiy PP PLC mapper",
        "dbms": !default_dbms,
        "re_match" : "^(.{2})(\\d+)\\.(.*)$",
        "table": "re.group(1)",
        "column": "re.group(3)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
            },
            "id": {
                "value": "re.group(2)",
                "type" : "string"
            }
        }

    }
}>

<new_policy  = {
    "transform": {
        "id": !policy_id_other,
        "name" : "Smart City PP PLC mapper - other",
        "dbms": !default_dbms,
        "re_match" : "([^.]*)\\.(.*)",
        "table": "re.group(1)",
        "column": "re.group(2)",
        "schema": {
            "timestamp": {
                "type": "timestamp",
                "bring": "[timestamp]",
                "default" : "now()"
            }
        }

    }
}>
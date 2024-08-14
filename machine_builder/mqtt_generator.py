import requests
import json



class MachineBuilder:
    def __init__(self):
        self.manufacturer = self.__user_input(prompt="Manufacturer", default="Orics", required=True)
        self.owner = self.__user_input(prompt="Owner", default="", required=True)
        self.serial = self.__user_input(prompt="Serial Number", default="", required=True)
        self.machine = self._user_input(prompt="Machine", default="", required=True)

        # Location of machine - if Geolocation, then Grafana can set map
        self.location = self.__user_input(prompt="Location", default="", required=False)

    def __user_input(self, prompt:str, default:str="", required:bool=True):
        full_promt = f"{prompt}: "
        if default:
            full_promt = f"{prompt} (Default: {default}): "
        while True:
            value = input(full_promt) or default
            if value != "" or required is False:
                return value
            print(f"{prompt} is required and cannot be empty.")

    def build_msg_client(self):
        topic = f"{self.manufacturer}/{self.machine}/{self.owner}/{self.serial}/#"
        msg_client = f"""<run msg client broker=local and log=false and topic=(
        \n\tname={topic} and
        \n\tdbms=orics and
        \n\ttable={machine} and
        \n\tcolumn.timestamp.timestamp="bring [ts]" and
        \n\tcolumn.serial_number.int=17415 and
        \n\tcolumn.seal_storage.float="bring [d][SealStage][0]" and
        \n\tcolumn.cy_min.float="bring [d][Cyc/Min][0]" and
        \n\tcolumn.batch_count.float="bring [d][BatchCount][0]" and
        \n\tcolumn.run_hours.float="bring [d][RunHours][0]" and
        \n\tcolumn.machine_state.float="bring [d][MachineState][0]" and
        \n\tcolumn.denester_in_cycle=(type=bool and value="bring [d][DenesterInCycle][0]") and
        \n\tcolumn.filler_stage.float="bring [d][FillerStage][0]" and
        \n\tcolumn.filler_cyc_time.float="bring [d][FillerCycTime][0]" and
        \n\tcolumn.seal_cyc_time.float="bring [d][SealCycTime][0]" and
        \n\tcolumn.heater1_setpoint.float="bring [d][Heater1Setpoint][0]" and
        \n\tcolumn.heater1_temp.float="bring [d][Heater1Temp][0]" and
        \n\tcolumn.cap_pick_in_cyc=(type=bool and value="bring [d][CapPickInCyc][0]") and
        \n\tcolumn.cap_press_in_cyc=(type=bool and value="bring [d][CapPressInCyc][0]") and
        \n\tcolumn.rotary_index_rdy=(type=bool and value="bring [d][RotaryIndexRDY][0]") and
        \n\tcolumn.rotary_index_run=(type=bool and value="bring [d][RotaryIndexRun][0]") and
        \n\tcolumn.rotary_index_i.float="bring [d][RotaryIndexI][0]" and
        \n\tcolumn.outfeed_conv_rdy=(type=bool and value="bring [d][OutfeedConvRDY][0]") and
        \n\tcolumn.outfeed_conv_run=(type=bool and value="bring [d][OutfeedConvRun][0]") and
        \n\tcolumn.outfeed_conv_i.float="bring [d][OutfeedConvI][0]" and
        \n\tcolumn.film_supply_rdy=(type=bool and value="bring [d][FilmSupplyRDY][0]") and
        \n\tcolumn.film_supply_run=(type=bool and value="bring [d][FilmSupplyRun][0]") and
        \n\tcolumn.film_supply_i.float="bring [d][FilmSupplyI][0]" and
        \n\tcolumn.film_adv_rdy=(type=bool and value="bring [d][FilmAdvRDY][0]") and
        \n\tcolumn.film_adv_run=(type=bool and value="bring [d][FilmAdvRun][0]") and
        \n\tcolumn.film_adv_i.float="bring [d][FilmAdvI][0]""""
        return msg_client



policy = {
   "machine": {
       "owner": owner,
       "manufacturer": manufacturer,
       "machine": machine,
       "serial_number": serial
    }
}

rest_conn = input("Operator REST Connection Info (default: 127.0.0.1:32149): ")
ledger_conn = input("Ledger Connection Info (default: 127.0.0.1:32048): ")

raw_policy = "<new_policy=%s>" % json.dumps(policy)

headers = {
    'command': 'blockchain push !new_policy',
    'User-Agent': 'AnyLog/1.23',
    'destination': ledger_conn
}


try:
    r = requests.post(url='http://%s' % rest_conn, headers=headers, data=raw_policy, auth=auth, timeout=timeout)
except Exception as e:
    print('Failed to POST policy against %s (Error; %s)' % (conn, e))
    status = False
else:
    if int(r.status_code) != 200:
        print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
        status = False
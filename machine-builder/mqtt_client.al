<run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
   name="Orics/R-50/HighlandFarms/17415/#" and
   dbms=orics and
   table=r_50 and
   column.timestamp.timestamp="bring [ts]" and
   column.serial_number.int=17415 and
   column.seal_storage.float="bring [d][SealStage][0]" and
   column.cy_min.float="bring [d][Cyc/Min][0]" and
   column.batch_count.float="bring [d][BatchCount][0]" and
   column.run_hours.float="bring [d][RunHours][0]" and
   column.machine_state.float="bring [d][MachineState][0]" and
   column.denester_in_cycle=(type=bool and value="bring [d][DenesterInCycle][0]") and
   column.filler_stage.float="bring [d][FillerStage][0]" and
   column.filler_cyc_time.float="bring [d][FillerCycTime][0]" and
   column.seal_cyc_time.float="bring [d][SealCycTime][0]" and
   column.heater1_setpoint.float="bring [d][Heater1Setpoint][0]" and
   column.heater1_temp.float="bring [d][Heater1Temp][0]" and
   column.cap_pick_in_cyc=(type=bool and value="bring [d][CapPickInCyc][0]") and
   column.cap_press_in_cyc=(type=bool and value="bring [d][CapPressInCyc][0]") and
   column.rotary_index_rdy=(type=bool and value="bring [d][RotaryIndexRDY][0]") and
   column.rotary_index_run=(type=bool and value="bring [d][RotaryIndexRun][0]") and
   column.rotary_index_i.float="bring [d][RotaryIndexI][0]" and
   column.outfeed_conv_rdy=(type=bool and value="bring [d][OutfeedConvRDY][0]") and
   column.outfeed_conv_run=(type=bool and value="bring [d][OutfeedConvRun][0]") and
   column.outfeed_conv_i.float="bring [d][OutfeedConvI][0]" and
   column.film_supply_rdy=(type=bool and value="bring [d][FilmSupplyRDY][0]") and
   column.film_supply_run=(type=bool and value="bring [d][FilmSupplyRun][0]") and
   column.film_supply_i.float="bring [d][FilmSupplyI][0]" and
   column.film_adv_rdy=(type=bool and value="bring [d][FilmAdvRDY][0]") and
   column.film_adv_run=(type=bool and value="bring [d][FilmAdvRun][0]") and
   column.film_adv_i.float="bring [d][FilmAdvI][0]"
)>
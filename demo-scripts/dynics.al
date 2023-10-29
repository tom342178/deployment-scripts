{"M40010":31954,"M40009":31954,"M40008":31954,"M40007":31954,"M40006":31954,"M40005":31954,"M40004":31954,"M40003":31954,"M40002":31954,"M40001":31954}	Q0
	{"Name":"fusion-1","Cpu":2,"MemoryTotal":4293861376,"MemoryAvailable":821567488}

<run mqtt client where broker=driver.cloudmqtt.com and port=18742 and user=hqpyyshb and password=bB38GEf93cPG and
    log=false and topic=(
        name=dynicsstatustest and
        dbms=!default_dbms and
        table=dynics_health and
        column.timestamp.timestamp=now and
        column.name=(type=str and value="bring [Name]") and
        column.cpu=(type=int and value="bring [Cpu]") and
        column.memory_total=(type=int and value="bring [MemoryTotal]") and
        column.memory_available=(type=int and value="bring [MemoryAvailable]")
    ) and topic=(
        name=dynicsmodbustest and
        dbms=!default_dbms and
        table=modbus and
        column.timestamp.timestamp=now and
        column.m40001=(type=int and value="bring [M40001]") and
        column.m40002=(type=int and value="bring [M40002]") and
        column.m40003=(type=int and value="bring [M40003]") and
        column.m40004=(type=int and value="bring [M40004]") and
        column.m40005=(type=int and value="bring [M40005]") and
        column.m40006=(type=int and value="bring [M40006]") and
        column.m40007=(type=int and value="bring [M40007]") and
        column.m40008=(type=int and value="bring [M40008]") and
        column.m40009=(type=int and value="bring [M40009]") and
        column.m40010=(type=int and value="bring [M40010]")
)>
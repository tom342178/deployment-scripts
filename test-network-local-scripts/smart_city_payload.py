import argparse
import json

import requests

DATA = ["KPL", "BF1", "BF2", "BF3", "BF4", "BSP", "BCT", "CBT", "CF1", "CF2", "CF3", "CSP", "CDT", "DCT", "DF1", "DF2",
        "DF3", "DF4", "DSP", "BG8", "BG9", "BG10", "BG11", "CG7", "CG12", "DG2", "DG3", "DG4", "DG5", "DG6"]

def check_policy(conn:str, db_name:str, table:str, monitor_id:str):
    """
    Check whether policy exists
    :args:
        conn:str - REST connection information
        db_name:str - logical database mane
        table:str - table namee
        monitor_id:str - mmonitor id
    :params:
        status:bool
        headers:dict - REST headers
        response:requests.GET - GET response
    :return:
        True - exists
        False - DNE
    """
    headers = {
        "command": f"blockchain get tag where dbms={db_name} and table={table} and monitor_id={monitor_id}",
        "User-Agent": "AnyLog/1.23"
    }
    status = True

    try:
        response = requests.get(url=f"http://{conn}", headers=headers)
        response.raise_for_status()
    except Exception as error:
        raise Exception
    else:
        if not response.json():
            status = False
    return status


def create_policy(conn:str, db_name:str, table:str, monitor_id:str):
    headers = {
        "command": "blockchain insert where policy=!new_policy and local=true and master=!ledger_conn",
        "User-Agent": "AnyLog/1.23"
    }

    policy = {
        "device": {
            "dbms": db_name,
            "table": table,
            "monitor_id": monitor_id
        }
    }

    new_policy = f"<new_policy={json.dumps(policy)}>"
    try:
        response = requests.post(url=f"http://{conn}", headers=headers, data=new_policy)
        response.raise_for_status()
    except Exception as error:
        raise Exception

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--conn', type=str, default="23.239.12.151:32349", help='REST conn to publish policy')
    parse.add_argument('--db-name', type=str, default='cos', help='logical database name')
    parse.add_argument('--table-name', type=str, default='pp_pm', help='table name')
    args = parse.parse_args()

    for id in DATA:
        is_policy = check_policy(conn=args.conn, db_name=args.db_name, table=args.table_name, monitor_id=id)
        if is_policy is False:
            create_policy(conn=args.conn, db_name=args.db_name, table=args.table_name, monitor_id=id)


if __name__ == '__main__':
    main()



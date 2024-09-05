import argparse
import requests


def __get_location():
    """
    Get geolocation information
    """
    r = requests.get("https://ipinfo.io/json")
    try:
        return r.json()
    except Exception as error:
        print(f"Failed to get geolocation (Error: {error})")


def __user_input():
    """
    Allow user to set user inputs + create policy
    """
    geolocation = __get_location()
    owner = None
    serial_number = None

    device_name = input("Device Name (default: R-50): ").strip() or "R-50"
    while owner is None:
        owner = input("Device Owner: ").strip()

    manufacturer = input("Manufacturer (default: Orics): ").strip() or "Orics"
    while serial_number is None:
        serial_number = input("Serial Number: ").strip()

    return {"machine": {
        "device": device_name,
        "manufacturer": manufacturer,
        "serial_number": serial_number,
        "owner": owner,
        "country": geolocation['country'],
        "region": geolocation['region'],
        "city": geolocation['city'],
        "loc": geolocation['loc']
    }}


def __publish_policy(conn:str, ledger_conn:str, policy:dict, auth:tuple=(), timeout:int=30)->bool:
    """
    Publish policy into a network via REST POST
    :args:
        conn:str - REST connection information
        ledger_conn:str - master node or blockchain ledger connection infromation
        policy_id:dict - policy to publish
        auth:tuple - rest authentication
        timeout:str - REST timeout
    """
    status = True

    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    if isinstance(policy, dict):  # convert policy to str if dict
        policy = json.dumps(policy)
    raw_policy = "<new_policy=%s>" % policy

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=raw_policy, auth=auth, timeout=timeout)
    except Exception as e:
        print('Failed to POST policy against %s (Error; %s)' % (conn, e))
        status = False
    else:
        if int(r.status_code) != 200:
            print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
            status = False

    return status


def main():
    """
    Declare machine policy
    :positional arguments:
        rest_conn             REST connection information
        ledger_conn           TCP master information
    :optional arguments:
        -h, --help            show this help message and exit
        -a AUTH, --auth         AUTH      REST authentication information (default: None)
        -t TIMEOUT, --timeout   TIMEOUT   REST timeout period (default: 30)
    :params:
        policy:dict - new policy to be added into blockchain
    :sample-policy:
        {
           "machine": {
              "name": "R-50",
              "owner": "HighlandFarms",
              "manufacturer": "Orics",
              "serial_number": 17415,
              "loc": "43.621302, -79.671353"
           }
        }
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rest_conn',       type=str,   default='127.0.0.1:2049', help='REST connection information')
    parser.add_argument('ledger_conn',     type=str,   default='127.0.0.1:2048', help='TCP master information')
    parser.add_argument('-a', '--auth',    type=str, default=None, help='REST authentication information')
    parser.add_argument('-t', '--timeout', type=int,   default=30,   help='REST timeout period')
    args = parser.parse_args()

    # connect to AnyLog
    auth = ()
    if args.auth is not None:
        auth = tuple(args.auth.split(','))

    policy = __user_input()
    __publish_policy(conn=args.rest_conn, ledger_conn=args.ledger_conn, policy=policy, auth=auth, timeout=args.timeout)


if __name__ == '__main__':
    main()
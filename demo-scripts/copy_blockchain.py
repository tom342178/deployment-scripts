import argparse
import json
import requests

def get_cmd()->list:
    """
    Execute `blockchain get` to get operators, clusters and their tables
    :params:
        headers:dict - REST headers
        r:requests.GET - REST request results
    :return:
        sub set of the blockchain consisting of cluster, operator, table as a list of python dictionaries
    """
    headers = {
        "command": "blockchain get (cluster, operator, table)",
        "User-Agent": "AnyLog/1.23"
    }

    try:
        r = requests.get(url='http://23.239.12.151:32349', headers=headers)
    except Exception as error:
        print(f"Failed to execute GET against 23.239.12.151:32349 (Error: {error})")
    else:
        if int(r.status_code) != 200:
            print(f"Failed to execute GET against 23.239.12.151:32349 (Network Error Code: {r.status_code})")
        else:
            try:
                return r.json()
            except Exception as error:
                print(f"Failed to extract results in JSON format from 23.239.12.151:32349 (Error: {error})")


def post_cmd(conn:str, ledger_conn:str, payload:dict)->bool:
    """
    Post policy to AnyLog node
    :args:
        conn:str - REST connection information
        ledger_conn:str - ledger connection
        payload:dict - dictionary of JSON policy to be added to the node
    :params:
        status:bool
        headers:dict - REST header information
        policy:str - serialized JSON of payload
        raw_policy:str - payload to be sent into AnyLog
        r:requests.POST - result from POST request
    :return:
        True - if success
        False - if fails
    """
    status = False
    headers = {
        'command': 'blockchain push !new_policy',
        'User-Agent': 'AnyLog/1.23',
        'destination': ledger_conn
    }

    if isinstance(payload, dict):  # convert policy to str if dict
        policy = json.dumps(payload)
        raw_policy = "<new_policy=%s>" % policy
    else:
        raw_policy = "<new_policy=%s>" % payload

    try:
        r = requests.post(url='http://%s' % conn, headers=headers, data=raw_policy)
    except Exception as e:
        print('Failed to POST policy against %s (Error; %s)' % (conn, e))
    else:
        if int(r.status_code) != 200:
            print('Failed to POST policy against %s (Network Error: %s)' % (conn, r.status_code))
        else:
            status = True

    return status


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('conn', type=str, default='127.0.0.1:32049', help='REST connection information')
    parse.add_argument('ledger_conn', type=str, default='127.0.0.1:32049', hel='ledger conn information (TCP connection)')
    args = parse.parse_args()

    payloads = get_cmd()
    for payload in payloads:
        post_cmd(conn=args.conn, ledger_conn=args.ledger_conn, payload=payload)


if __name__ == '__main__':
    main()
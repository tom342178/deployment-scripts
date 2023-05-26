import argparse
import pytest
import re
import requests

def __validate_conn_pattern(conn: str) -> str:
    """
    Validate connection information format is connect
    :valid formats:
        127.0.0.1:32049
        user:passwd@127.0.0.1:32049
    :args:
        conn:str - REST connection information
    :params:
        pattern1:str - compiled pattern 1 (127.0.0.1:32049)
        pattern2:str - compiled pattern 2 (user:passwd@127.0.0.1:32049)
    :return:
        if fails raises Error
        if success returns conn
    """
    pattern1 = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')
    pattern2 = re.compile(r'^\w+:\w+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$')

    if not pattern1.match(conn) and not pattern2.match(conn):
        raise argparse.ArgumentTypeError(f'Invalid REST connection format: {conn}')

    return conn

@pytest.fixture
def parser()->dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=__validate_conn_pattern, default='23.239.12.151:32349', help="REST connection information (example: {user}:{password}@{ip}:{port})")
    parser.add_argument('--timeout', type=int, default=30)


def execute_query(conn:str, auth:tuple, timeout:int, headers:dict)->requests.Request:
    """
    Execute REST request against a node
    :args:
        conn:str - REST connection information
        auth:tuple - REST authentication information
        timeout:int - REST timeout
        headers:dict - REST headers
    :params:
        r:requests.Request - request return
    :exception:
        1. query fails to execute
        2. request returns a status_code != 200
    :return:
        raw request results
    """
    try:
        r = requests.get(url=f"http://{conn}", auth=auth, timeout=timeout, headers=headers)
    except Exception as error:
        pytest.fail(f"Failed to execute `{headers['command']}` against {conn} (Error: {error})", pytrace=True)
    else:
        if int(r.status_code) != 200:
            pytest.fail(f"Failed to execute `{headers['command']}` against {conn} (Network Error: {r.status_code})", pytrace=True)
    return r


def validate_status(conn:str, auth:tuple, timeout:int)->bool:
    """
    Validate whether the node is accessible (via REST)
    :args:
        conn:str - REST connection information
        auth:tuple - REST authentication information
        timeout:int - REST timeout
    :params:
        status:bool
        headers:dict - REST headers
    :return:
        if success returns True
        else returns False
        if fails returns an exception
    """
    status = True
    headers = {
        "command": "get status",
        "User-Agent": "AnyLog/1.23"
    }

    r = execute_query(conn=conn, auth=auth, timeout=timeout, headers=headers)
    if 'running' in r.text and 'not' not in r.text:
        status = True

    return status
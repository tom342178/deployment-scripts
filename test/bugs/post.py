"""
Expect: Success without any issues
Actual: currently returns
    (False, '("Connection broken: InvalidChunkLength(got length b\'\', 0 bytes read)", InvalidChunkLength(got length b\'\', 0 bytes read))')
"""
import requests


def post(conn:str, headers: dict, payload: str = None):
    """
    Execute POST command against AnyLog. payload is required under the following conditions:
        1. payload can be data that you want to add into AnyLog, in which case you should also have an
            MQTT client of type REST running on said node
        2. payload can be a policy you'd like to add into the blockchain
        3. payload can be a policy you'd like to remove from the blockchain
            note only works with Master, cannot remove a policy on a real blockchain like Ethereum.
    :args:
        headers:dict - request headers
        payloads:str - data to post
    :params:
        r:requests.response - response from requests
        error:str - If exception during error
    :return:
        r, error
    """
    error = None
    try:
        r = requests.post('http://%s' % conn, headers=headers, data=payload, auth=(),
                          timeout=30)
    except Exception as e:
        error = str(e)
        r = False
    else:
        if int(r.status_code) != 200:
            error = str(r.status_code)
            r = False

    return r, error


def main(conn:str):
    header = {
        "command": "connect dbms test2 where type=sqlite",
        "User-Agent": "AnyLog/1.23"
    }

    print(post(conn=conn, headers=header, payload=None))


if __name__ == '__main__':
    main(conn='10.0.0.78:7849')
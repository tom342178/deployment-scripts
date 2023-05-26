
import pytest
import support

CONN = '10.0.0.184:32349'
AUTH = None
TIMEOUT = 30

def execute_query(conn:str, auth:tuple, timeout:int, query:str):
    headers = {
        "command": query,
        "User-Agent": "AnyLog/1.23",
        "destination": "network"
    }

    r = support.execute_query(conn=conn, auth=auth, timeout=timeout, headers=headers)
    try:
        output = r.json()
    except Exception as error:
        pytest.fail(f"Failed extract results for `{headers['command']} (Error: {error})", pytrace=True)
    if 'Query' not in output:
        pytest.fail(f"Failed to for `{headers['command']} (Error: Missing `Query` key in outputted results)", pytrace=True)
    # else:
    #     pytest.fail(output, pytrace=False)

    return output['Query']

@pytest.mark.skipif(not support.validate_status(conn=CONN, auth=AUTH, timeout=TIMEOUT), reason='No connection')
class TestValues:
    """
    REST based testing to validate aggregate functions (against a single table/database) work correctly
    """
    def setup_class(self):
        self.conn = CONN
        self.auth = AUTH
        self.timeout = TIMEOUT
        self.base_query = f"sql test format=json and stat=false "

    def test_row_count(self):
        """
        Validate number of rows in ping sensor
        :query:
            SELECT COUNT(*) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT COUNT(*) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert  result[0]['result'] == 10000

    def test_min_value(self):
        """
        Validate MIN value for ping sensor
        :query:
            SELECT MIN(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT MIN(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 0

    def test_max_value(self):
        """
        Validate MAX value for ping sensor
        :query:
            SELECT MAX(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT MAX(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 49

    def test_sum_value(self):
        """
        Validate SUM value for ping sensor
        :query:
            SELECT SUM(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT SUM(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 152143.64999999988

    def test_avg_value(self):
        """
        Validate AVG value for ping sensor
        :query:
            SELECT AVG(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT AVG(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 152143.64999999988/10000


    def test_distinct_string(self):
        """
        Validate DISTINCT string for ping sensor
        :query:
            SELECT DISTINCT(device_name) as result FROM ping_sensor
        """
        result_set = []
        query = self.base_query + ' "SELECT DISTINCT(device_name) as result FROM ping_sensor ORDER BY result;"'
        results = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        for result in results:
            result_set.append(result['result'])
        assert result_set == ['ADVA FSP3000R7', 'Catalyst 3500XL', 'GOOGLE_PING', 'Ubiquiti OLT', 'VM Lit SL NMS']

    def test_distinct_uuid(self):
        """
        Validate DISTINCT uuid for ping sensor
        :query:
            SELECT DISTINCT(parentelement) as result FROM ping_sensor
        """
        result_set = []
        query = self.base_query + ' "SELECT DISTINCT(parentelement) as result FROM ping_sensor ORDER BY result;"'
        results = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        for result in results:
            result_set.append(result['result'])
        assert result_set == ['1ab3b14e-93b1-11e9-b465-d4856454f4ba','62e71893-92e0-11e9-b465-d4856454f4ba',
                              '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'd515dccb-58be-11ea-b46d-d4856454f4ba',
                              'f0bd0832-a81e-11ea-b46d-d4856454f4ba']

    def test_count_distinct_string(self):
        """
        Validate COUNT-DISTINCT string for ping sensor
        :query:
            SELECT COUNT(DISTINCT(device_name)) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT COUNT(DISTINCT(device_name)) as result FROM ping_sensor ORDER BY result;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 5


    def test_count_distinct_uuid(self):
        """
        Validate COUNT-DISTINCT UUID for ping sensor
        :query:
            SELECT COUNT(DISTINCT(parentelement)) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT COUNT(DISTINCT(parentelement)) as result FROM ping_sensor ORDER BY result;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0]['result'] == 5


    def test_where_timestamp(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp
        :query:
            SELECT
                MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313';
        """
        query = (self.base_query + "SELECT MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313';")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)

        assert result[0] == {'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313',
                             'min_value': 0.22, 'avg_value': 10.007142857142856, 'max_value': 40.73, 'row_count': 14}


    def test_where_string(self):
        """
        Validate results are correct with a WHERE condition on a given string
        :query:
            SELECT
                MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count
            FROM
                ping_sensor
            WHERE
                device_name='GOOGLE_PING'
        """
        query = (self.base_query + "SELECT MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value, "
                                   +"COUNT(*) AS row_count FROM ping_sensor WHERE device_name='ADVA FSP3000R7';")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0] == {'min_value': 0.0, 'avg_value': 1.9717499999999992, 'max_value': 4.0, 'row_count': 2040}


    def test_where_uuid(self):
        """
        Validate results are correct with a WHERE condition on a given uuid
        :query:
            SELECT
                MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count
            FROM
                ping_sensor
            WHERE
                parentelement='62e71893-92e0-11e9-b465-d4856454f4ba'
        """
        query = (self.base_query + "SELECT MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value, "
                                   +"COUNT(*) AS row_count FROM ping_sensor WHERE parentelement='62e71893-92e0-11e9-b465-d4856454f4ba';")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result[0] == {'min_value': 0.0, 'avg_value': 1.9717499999999992, 'max_value': 4.0, 'row_count': 2040}


    def test_group_string(self):
        """
        Validate data is correct when grouping by string column
        :query:
            SELECT
                device_name, MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value,
                COUNT(*) as row_count
            FROM
                ping_sensor
            GROUP BY
                device_name;
        """
        query = (self.base_query + "SELECT device_name, MIN(value) AS min_value, AVG(value) AS avg_value, "
                +"MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor GROUP BY device_name ORDER BY device_name ASC")

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_value': 0.0, 'avg_value': 1.9717499999999992,
                           'max_value': 4.0, 'row_count': 2040},
                          {'device_name': 'Catalyst 3500XL', 'min_value': 0.03, 'avg_value': 24.462562025316483,
                           'max_value': 48.97, 'row_count': 1975},
                          {'device_name': 'GOOGLE_PING', 'min_value': 2.01, 'avg_value': 19.511102680829545,
                           'max_value': 36.99, 'row_count': 1977},
                          {'device_name': 'Ubiquiti OLT', 'min_value': 0.05, 'avg_value': 25.059047856430723,
                           'max_value': 49.0, 'row_count': 2006},
                          {'device_name': 'VM Lit SL NMS', 'min_value': 0.0, 'avg_value': 5.477432567432567,
                           'max_value': 11.0, 'row_count': 2002}
                          ]


    def test_group_uuid(self):
        """
        Validate data is correct when grouping by uuid column
        :query:
            SELECT
                parentelement, MIN(value) AS min_value, AVG(value) AS avg_value, MAX(value) AS max_value,
                COUNT(*) as row_count
            FROM
                ping_sensor
            GROUP BY
                parentelement;
        """
        query = (self.base_query + "SELECT parentelement, MIN(value) AS min_value, AVG(value) AS avg_value, "
                +"MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor GROUP BY parentelement ORDER BY parentelement DESC")

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)
        assert result == [{'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_value': 2.01,
                           'avg_value': 19.51110268082956, 'max_value': 36.99, 'row_count': 1977},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_value': 0.05,
                           'avg_value': 25.059047856430684, 'max_value': 49.0, 'row_count': 2006},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_value': 0.03,
                           'avg_value': 24.462562025316497, 'max_value': 48.97, 'row_count': 1975},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_value': 0.0,
                           'avg_value': 1.971750000000001, 'max_value': 4.0, 'row_count': 2040},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_value': 0.0,
                           'avg_value': 5.477432567432568, 'max_value': 11.0, 'row_count': 2002}]


    def test_where_timestamp_group_string(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp grouped by string
        :query:
            SELECT
                device_name, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313'
            GROUP BY
                device_name;
        """
        query = (self.base_query + "SELECT device_name, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313' GROUP BY device_name;")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-17 14:12:46.411057',
                           'max_ts': '2022-02-17 14:53:47.539667', 'min_value': 0.22, 'avg_value': 1.536,
                           'max_value': 2.23, 'row_count': 5},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-02-17 14:45:46.402028',
                           'max_ts': '2022-02-17 14:51:47.520320', 'min_value': 10.64, 'avg_value': 16.715,
                           'max_value': 22.79, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-17 14:21:46.798998',
                           'max_ts': '2022-02-17 14:21:46.798998', 'min_value': 23.88,
                           'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-17 14:28:46.807520',
                           'max_ts': '2022-02-17 14:28:46.807520', 'min_value': 40.73, 'avg_value': 40.73,
                           'max_value': 40.73, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-17 14:02:46.088401',
                           'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 1.19, 'avg_value': 6.876,
                           'max_value': 10.13, 'row_count': 5}]


    def test_where_timestamp_group_uuid(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp grouped by uuid
        :query:
            SELECT
                parentelement, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313'
            GROUP BY
                parentelement;
        """
        query = (self.base_query + "SELECT parentelement, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313' GROUP BY parentelement;")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba',
                           'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313',
                           'min_value': 1.19, 'avg_value': 6.876, 'max_value': 10.13, 'row_count': 5},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba',
                           'min_ts': '2022-02-17 14:12:46.411057', 'max_ts': '2022-02-17 14:53:47.539667',
                           'min_value': 0.22, 'avg_value': 1.536, 'max_value': 2.23, 'row_count': 5},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba',
                           'min_ts': '2022-02-17 14:45:46.402028', 'max_ts': '2022-02-17 14:51:47.520320',
                           'min_value': 10.64, 'avg_value': 16.715, 'max_value': 22.79, 'row_count': 2},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba',
                           'min_ts': '2022-02-17 14:28:46.807520', 'max_ts': '2022-02-17 14:28:46.807520',
                           'min_value': 40.73, 'avg_value': 40.73, 'max_value': 40.73, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba',
                           'min_ts': '2022-02-17 14:21:46.798998', 'max_ts': '2022-02-17 14:21:46.798998',
                           'min_value': 23.88, 'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1}]


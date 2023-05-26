import pytest
import unittest
import support


def execute_query(conn:str, auth:tuple, timeout:int, destination:str, query:str):
    headers = {
        "command": query,
        "User-Agent": "AnyLog/1.23",
        "destination": destination
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


@pytest.mark.usefixtures("pass_parameters")
class TestValues(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        cls.base_query = f"sql test format=json and stat=false and include=(percentagecpu_sensor) and extend=(@table_name as table) "

    def test_row_count(self):
        """
        Validate number of rows in ping sensor
        :query:
            SELECT COUNT(*) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT COUNT(*) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

=======
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
        assert result == [{'table': 'percentagecpu_sensor', 'result': 10000},
                          {'table': 'ping_sensor', 'result': 10000}]

    def test_min_value(self):
        """
        Validate MIN value for ping sensor
        :query:
            SELECT MIN(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT MIN(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

=======
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
        assert result == [{'table': 'percentagecpu_sensor', 'result': 0.0},
                          {'table': 'ping_sensor', 'result': 0.0}]

    def test_max_value(self):
        """
        Validate MAX value for ping sensor
        :query:
            SELECT MAX(value) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT MAX(value) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
        assert result == [{'table': 'percentagecpu_sensor', 'result': 99.99},
<<<<<<< HEAD
                          {'table': 'ping_sensor', 'result': 49.0}]
=======
                          {'table': 'ping_sensor', 'result': 49}]
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

    def test_sum_value(self):
        """
        Validate SUM value for ping sensor
        :query:
            SELECT SUM(value)::float(6) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT SUM(value)::float(6) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

        assert result == [{'table': 'percentagecpu_sensor', 'result': 502823.34},
                          {'table': 'ping_sensor', 'result': 152143.65}]

        assert result[0]['result'] + result[1]['result'] == 654966.99

=======
        assert result == [{'table': 'percentagecpu_sensor', 'result': 502823.34},
                          {'table': 'ping_sensor', 'result': 152143.65}]

>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
    def test_avg_value(self):
        """
        Validate AVG value for ping sensor
        :query:
            SELECT AVG(value)::float(6) as result FROM ping_sensor
        """
        query = self.base_query + ' "SELECT AVG(value)::float(6) as result FROM ping_sensor;"'
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

        assert result == [{'table': 'percentagecpu_sensor', 'result': 50.282334},
                          {'table': 'ping_sensor', 'result': 15.214365}]


=======
        assert result == [{'table': 'percentagecpu_sensor', 'result': 50.282334},
                          {'table': 'ping_sensor', 'result': 15.214365}]

>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
    def test_where_timestamp(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp
        :query:
            SELECT
                MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313';
        """
        query = (self.base_query + "SELECT MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313';")
<<<<<<< HEAD
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-02-17 14:01:51.249653', 'max_ts': '2022-02-17 14:54:51.252830', 'min_value': 1.94, 'avg_value': 37.55625, 'max_value': 82.34, 'row_count': 8},
                          {'table': 'ping_sensor', 'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 0.22, 'avg_value': 10.007143, 'max_value': 40.73, 'row_count': 14}]
=======

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
        assert result ==  [{'table': 'percentagecpu_sensor', 'min_ts': '2022-02-17 14:01:51.249653', 'max_ts': '2022-02-17 14:54:51.252830', 'min_value': 1.94, 'avg_value': 37.55625, 'max_value': 82.34, 'row_count': 8},
                           {'table': 'ping_sensor', 'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 0.22, 'avg_value': 10.007143, 'max_value': 40.73, 'row_count': 14}]

>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

    def test_where_string(self):
        """
        Validate results are correct with a WHERE condition on a given string
        :query:
            SELECT
                MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count
            FROM
                ping_sensor
            WHERE
                device_name='GOOGLE_PING'
        """
        query = (self.base_query + "SELECT MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, "
                                   +"COUNT(*) AS row_count FROM ping_sensor WHERE device_name='ADVA FSP3000R7';")
<<<<<<< HEAD
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_value': 0.0, 'avg_value': 50.20932, 'max_value': 99.99, 'row_count': 1942},
                          {'table': 'ping_sensor', 'min_value': 0.0, 'avg_value': 1.97175, 'max_value': 4.0, 'row_count': 2040}]
=======

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)

        assert result ==  [{'table': 'percentagecpu_sensor', 'min_value': 0.0, 'avg_value': 50.20932, 'max_value': 99.99, 'row_count': 1942},
                           {'table': 'ping_sensor', 'min_value': 0.0, 'avg_value': 1.97175, 'max_value': 4.0, 'row_count': 2040}]
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

    def test_where_uuid(self):
        """
        Validate results are correct with a WHERE condition on a given uuid
        :query:
            SELECT
                MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count
            FROM
                ping_sensor
            WHERE
                parentelement='62e71893-92e0-11e9-b465-d4856454f4ba'
        """
        query = (self.base_query + "SELECT MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, "
                                   +"COUNT(*) AS row_count FROM ping_sensor WHERE parentelement='62e71893-92e0-11e9-b465-d4856454f4ba';")
<<<<<<< HEAD

=======
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_value': 0.0, 'avg_value': 50.20932, 'max_value': 99.99, 'row_count': 1942},
                          {'table': 'ping_sensor', 'min_value': 0.0, 'avg_value': 1.97175, 'max_value': 4.0, 'row_count': 2040}]

<<<<<<< HEAD
=======

>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
    def test_group_string(self):
        """
        Validate data is correct when grouping by string column
        :query:
            SELECT
                device_name, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value,
                COUNT(*) as row_count
            FROM
                ping_sensor
            GROUP BY
                device_name;
        """
        query = (self.base_query + "SELECT device_name, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, "
                +"MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor GROUP BY device_name ORDER BY device_name ASC")

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
        assert result == [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_value': 0.0, 'avg_value': 50.20932, 'max_value': 99.99, 'row_count': 1942},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_value': 0.0, 'avg_value': 1.97175, 'max_value': 4.0, 'row_count': 2040},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_value': 0.0, 'avg_value': 50.536835, 'max_value': 99.94, 'row_count': 1959},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_value': 0.03, 'avg_value': 24.462562, 'max_value': 48.97, 'row_count': 1975},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_value': 0.02, 'avg_value': 50.498919, 'max_value': 99.94, 'row_count': 2035},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_value': 2.01, 'avg_value': 19.511103, 'max_value': 36.99, 'row_count': 1977},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_value': 0.07, 'avg_value': 49.99139, 'max_value': 99.9, 'row_count': 2014},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_value': 0.05, 'avg_value': 25.059048, 'max_value': 49.0, 'row_count': 2006},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_value': 0.02, 'avg_value': 50.179132, 'max_value': 99.96, 'row_count': 2050},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_value': 0.0, 'avg_value': 5.477433, 'max_value': 11.0, 'row_count': 2002}]

<<<<<<< HEAD
=======


>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
    def test_group_uuid(self):
        """
        Validate data is correct when grouping by uuid column
        :query:
            SELECT
                parentelement, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, MAX(value) AS max_value,
                COUNT(*) as row_count
            FROM
                ping_sensor
            GROUP BY
                parentelement;
        """
        query = (self.base_query + "SELECT parentelement, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value, "
                +"MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor GROUP BY parentelement ORDER BY parentelement DESC")

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

=======
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
        assert result == [{'table': 'percentagecpu_sensor', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_value': 0.02, 'avg_value': 50.498919, 'max_value': 99.94, 'row_count': 2035},
                          {'table': 'ping_sensor', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_value': 2.01, 'avg_value': 19.511103, 'max_value': 36.99, 'row_count': 1977},
                          {'table': 'percentagecpu_sensor', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_value': 0.07, 'avg_value': 49.99139, 'max_value': 99.9, 'row_count': 2014},
                          {'table': 'ping_sensor', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_value': 0.05, 'avg_value': 25.059048, 'max_value': 49.0, 'row_count': 2006},
                          {'table': 'percentagecpu_sensor', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_value': 0.0, 'avg_value': 50.536835, 'max_value': 99.94, 'row_count': 1959},
                          {'table': 'ping_sensor', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_value': 0.03, 'avg_value': 24.462562, 'max_value': 48.97, 'row_count': 1975},
                          {'table': 'percentagecpu_sensor', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_value': 0.0, 'avg_value': 50.20932, 'max_value': 99.99, 'row_count': 1942},
                          {'table': 'ping_sensor', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_value': 0.0, 'avg_value': 1.97175, 'max_value': 4.0, 'row_count': 2040},
                          {'table': 'percentagecpu_sensor', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_value': 0.02, 'avg_value': 50.179132, 'max_value': 99.96, 'row_count': 2050},
                          {'table': 'ping_sensor', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_value': 0.0, 'avg_value': 5.477433, 'max_value': 11.0, 'row_count': 2002}]

    def test_where_timestamp_group_string(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp grouped by string
        :query:
            SELECT
                device_name, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313'
            GROUP BY
                device_name;
        """
        query = (self.base_query + "SELECT device_name, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313' GROUP BY device_name;")
<<<<<<< HEAD
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-17 14:08:51.617237', 'max_ts': '2022-02-17 14:38:52.412542', 'min_value': 17.86, 'avg_value': 48.89, 'max_value': 82.34, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-17 14:24:51.965469', 'max_ts': '2022-02-17 14:24:51.965469', 'min_value': 57.61, 'avg_value': 57.61, 'max_value': 57.61, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-17 14:03:51.578110', 'max_ts': '2022-02-17 14:18:51.258845', 'min_value': 1.94, 'avg_value': 18.2, 'max_value': 34.46, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-17 14:01:51.249653', 'max_ts': '2022-02-17 14:54:51.252830', 'min_value': 12.37, 'avg_value': 29.885, 'max_value': 47.4, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-17 14:12:46.411057', 'max_ts': '2022-02-17 14:53:47.539667', 'min_value': 0.22, 'avg_value': 1.536, 'max_value': 2.23, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-02-17 14:45:46.402028', 'max_ts': '2022-02-17 14:51:47.520320', 'min_value': 10.64, 'avg_value': 16.715, 'max_value': 22.79, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-17 14:21:46.798998', 'max_ts': '2022-02-17 14:21:46.798998', 'min_value': 23.88, 'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-17 14:28:46.807520', 'max_ts': '2022-02-17 14:28:46.807520', 'min_value': 40.73, 'avg_value': 40.73, 'max_value': 40.73, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 1.19, 'avg_value': 6.876, 'max_value': 10.13, 'row_count': 5}]
=======

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
        assert result ==  [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-17 14:08:51.617237', 'max_ts': '2022-02-17 14:38:52.412542', 'min_value': 17.86, 'avg_value': 48.89, 'max_value': 82.34, 'row_count': 3},
                           {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-17 14:24:51.965469', 'max_ts': '2022-02-17 14:24:51.965469', 'min_value': 57.61, 'avg_value': 57.61, 'max_value': 57.61, 'row_count': 1},
                           {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-17 14:03:51.578110', 'max_ts': '2022-02-17 14:18:51.258845', 'min_value': 1.94, 'avg_value': 18.2, 'max_value': 34.46, 'row_count': 2},
                           {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-17 14:01:51.249653', 'max_ts': '2022-02-17 14:54:51.252830', 'min_value': 12.37, 'avg_value': 29.885, 'max_value': 47.4, 'row_count': 2},
                           {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-17 14:12:46.411057', 'max_ts': '2022-02-17 14:53:47.539667', 'min_value': 0.22, 'avg_value': 1.536, 'max_value': 2.23, 'row_count': 5},
                           {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-02-17 14:45:46.402028', 'max_ts': '2022-02-17 14:51:47.520320', 'min_value': 10.64, 'avg_value': 16.715, 'max_value': 22.79, 'row_count': 2},
                           {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-17 14:21:46.798998', 'max_ts': '2022-02-17 14:21:46.798998', 'min_value': 23.88, 'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1},
                           {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-17 14:28:46.807520', 'max_ts': '2022-02-17 14:28:46.807520', 'min_value': 40.73, 'avg_value': 40.73, 'max_value': 40.73, 'row_count': 1},
                           {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 1.19, 'avg_value': 6.876, 'max_value': 10.13, 'row_count': 5}]
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

    def test_where_timestamp_group_uuid(self):
        """
        Validate results are correct with a WHERE condition on a given timestamp grouped by uuid
        :query:
            SELECT
                parentelement, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, AVG(value)::float(6) AS avg_value,
                MAX(value) AS max_value, COUN(*) AS row_count
            FROM
                ping_sensor
            WHERE
                timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313'
            GROUP BY
                parentelement;
        """
        query = (self.base_query + "SELECT parentelement, MIN(timestamp) AS min_ts, MAX(timestamp) AS max_ts, MIN(value) AS min_value, "
                +"AVG(value)::float(6) AS avg_value, MAX(value) AS max_value, COUNT(*) AS row_count FROM ping_sensor WHERE "
                +"timestamp >= '2022-02-17 14:01:51.249653' AND timestamp <= '2022-02-17 14:55:47.250313' GROUP BY parentelement;")
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination, query=query)
<<<<<<< HEAD

=======
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7
        assert result == [{'table': 'percentagecpu_sensor', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-17 14:01:51.249653', 'max_ts': '2022-02-17 14:54:51.252830', 'min_value': 12.37, 'avg_value': 29.885, 'max_value': 47.4, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-17 14:08:51.617237', 'max_ts': '2022-02-17 14:38:52.412542', 'min_value': 17.86, 'avg_value': 48.89, 'max_value': 82.34, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-17 14:03:51.578110', 'max_ts': '2022-02-17 14:18:51.258845', 'min_value': 1.94, 'avg_value': 18.2, 'max_value': 34.46, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-17 14:24:51.965469', 'max_ts': '2022-02-17 14:24:51.965469', 'min_value': 57.61, 'avg_value': 57.61, 'max_value': 57.61, 'row_count': 1},
                          {'table': 'ping_sensor', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-17 14:02:46.088401', 'max_ts': '2022-02-17 14:55:47.250313', 'min_value': 1.19, 'avg_value': 6.876, 'max_value': 10.13, 'row_count': 5},
                          {'table': 'ping_sensor', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-17 14:12:46.411057', 'max_ts': '2022-02-17 14:53:47.539667', 'min_value': 0.22, 'avg_value': 1.536, 'max_value': 2.23, 'row_count': 5},
                          {'table': 'ping_sensor', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-17 14:45:46.402028', 'max_ts': '2022-02-17 14:51:47.520320', 'min_value': 10.64, 'avg_value': 16.715, 'max_value': 22.79, 'row_count': 2},
                          {'table': 'ping_sensor', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-17 14:28:46.807520', 'max_ts': '2022-02-17 14:28:46.807520', 'min_value': 40.73, 'avg_value': 40.73, 'max_value': 40.73, 'row_count': 1},
<<<<<<< HEAD
                          {'table': 'ping_sensor', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-17 14:21:46.798998', 'max_ts': '2022-02-17 14:21:46.798998', 'min_value': 23.88, 'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1}]
=======
                          {'table': 'ping_sensor', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-17 14:21:46.798998', 'max_ts': '2022-02-17 14:21:46.798998', 'min_value': 23.88, 'avg_value': 23.88, 'max_value': 23.88, 'row_count': 1}]
>>>>>>> 092473e91cf7a7f8cfcc7fb5f108be000a111fc7

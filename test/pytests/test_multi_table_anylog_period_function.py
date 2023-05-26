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
        cls.base_query = f"sql test format=json and stat=false and include=(percentagecpu_sensor) "

    def test_period_30second(self):
        """
        SELECT
            device_name, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(second, 30, NOW(), timestamp)
        GROUP BY
            device_name
        """
        query = (self.base_query + ' "SELECT device_name, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                +"MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                +'WHERE period(second, 30, NOW(), timestamp) GROUP BY device_name"')
        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_val': 0.0, 'avg_val': 23.190861, 'max_val': 99.59, 'sum_val': 13728.99, 'row_count': 592},
                          {'device_name': 'Catalyst 3500XL', 'min_val': 0.46, 'avg_val': 37.803917, 'max_val': 99.92, 'sum_val': 22682.35, 'row_count': 600},
                          {'device_name': 'GOOGLE_PING', 'min_val': 0.34, 'avg_val': 32.56441, 'max_val': 99.15, 'sum_val': 20157.37, 'row_count': 619},
                          {'device_name': 'Ubiquiti OLT', 'min_val': 0.11, 'avg_val': 36.498683, 'max_val': 99.63, 'sum_val': 21899.21, 'row_count': 600},
                          {'device_name': 'VM Lit SL NMS', 'min_val': 0.01, 'avg_val': 26.625376, 'max_val': 99.86, 'sum_val': 17333.12, 'row_count': 651}]

    def test_period_60second(self):
        """
        SELECT
            device_name, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(second, 60, NOW(), timestamp)
        GROUP BY
            device_name
        """
        query = (self.base_query + ' "SELECT device_name, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(second, 60, NOW(), timestamp) GROUP BY device_name"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_val': 0.0, 'avg_val': 23.190861, 'max_val': 99.59, 'sum_val': 13728.99, 'row_count': 592},
                          {'device_name': 'Catalyst 3500XL', 'min_val': 0.46, 'avg_val': 37.803917, 'max_val': 99.92, 'sum_val': 22682.35, 'row_count': 600},
                          {'device_name': 'GOOGLE_PING', 'min_val': 0.34, 'avg_val': 32.56441, 'max_val': 99.15, 'sum_val': 20157.37, 'row_count': 619},
                          {'device_name': 'Ubiquiti OLT', 'min_val': 0.11, 'avg_val': 36.498683, 'max_val': 99.63, 'sum_val': 21899.21, 'row_count': 600},
                          {'device_name': 'VM Lit SL NMS', 'min_val': 0.01, 'avg_val': 26.625376, 'max_val': 99.86, 'sum_val': 17333.12, 'row_count': 651}]

    def test_period_60second_vs_1minute(self):
        """
        SELECT
            device_name, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(second, 60, NOW(), timestamp)
        GROUP BY
            device_name
        """
        query = (self.base_query + ' "SELECT device_name, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(second, 60, NOW(), timestamp) GROUP BY device_name"')
        result_60sec = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        query = (self.base_query + ' "SELECT device_name, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(minute, 1, NOW(), timestamp) GROUP BY device_name"')
        result_1min = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                     query=query)

        assert result_60sec == result_1min

    def test_period_1minute(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(minute, 1, NOW(), timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT parentelement, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(minute, 1, NOW(), timestamp) GROUP BY parentelement"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 26.625376, 'max_val': 99.86, 'sum_val': 17333.12, 'row_count': 651},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 23.190861, 'max_val': 99.59, 'sum_val': 13728.99, 'row_count': 592},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 37.803917, 'max_val': 99.92, 'sum_val': 22682.35, 'row_count': 600},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 36.498683, 'max_val': 99.63, 'sum_val': 21899.21, 'row_count': 600},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 0.34, 'avg_val': 32.56441, 'max_val': 99.15, 'sum_val': 20157.37, 'row_count': 619}]

    def test_period_30minute(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(minute, 30, NOW(), timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT parentelement, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(minute, 30, NOW(), timestamp) GROUP BY parentelement"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 26.625376, 'max_val': 99.86, 'sum_val': 17333.12, 'row_count': 651},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 23.190861, 'max_val': 99.59, 'sum_val': 13728.99, 'row_count': 592},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 37.803917, 'max_val': 99.92, 'sum_val': 22682.35, 'row_count': 600},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 36.498683, 'max_val': 99.63, 'sum_val': 21899.21, 'row_count': 600},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 0.34, 'avg_val': 32.56441, 'max_val': 99.15, 'sum_val': 20157.37, 'row_count': 619}]

    @pytest.mark.skip()
    def test_period_1hour(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(hour, 1, NOW(), timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT parentelement, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(hour, 1, NOW(), timestamp) GROUP BY parentelement"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 26.625376, 'max_val': 99.86, 'sum_val': 17333.12, 'row_count': 651},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 23.190861, 'max_val': 99.59, 'sum_val': 13728.99, 'row_count': 592},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 37.803917, 'max_val': 99.92, 'sum_val': 22682.35, 'row_count': 600},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 36.498683, 'max_val': 99.63, 'sum_val': 21899.21, 'row_count': 600},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 0.34, 'avg_val': 32.56441, 'max_val': 99.15, 'sum_val': 20157.37, 'row_count': 619}]

    def test_period_6hour(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(hour, 6, '2022-12-31 00:00:00', timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT parentelement, MIN(value) AS min_val, AVG(value)::float(6) AS avg_val, '
                 + "MAX(value) AS max_val, SUM(value)::float(6) AS sum_val, COUNT(value) AS row_count FROM ping_sensor "
                 + 'WHERE period(hour, 6, \'2022-12-31 00:00:00\', timestamp) GROUP BY parentelement"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 19.75, 'avg_val': 19.75, 'max_val': 19.75, 'sum_val': 19.75, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 1.18, 'avg_val': 32.01, 'max_val': 94.27, 'sum_val': 288.09, 'row_count': 9},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 7.76, 'avg_val': 51.488571, 'max_val': 88.31, 'sum_val': 360.42, 'row_count': 7},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 5.54, 'avg_val': 38.38, 'max_val': 91.31, 'sum_val': 345.42, 'row_count': 9},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 8.12, 'avg_val': 25.474, 'max_val': 75.9, 'sum_val': 127.37, 'row_count': 5}]

    def test_period_12hour(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(hour, 12, '2022-12-31 00:00:00', timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT timestamp, device_name, value FROM ping_sensor '
                 + 'WHERE period(hour, 12, \'2022-12-31 00:00:00\', timestamp) ORDER BY timestamp"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'timestamp': '2022-04-16 08:35:51.290166', 'device_name': 'GOOGLE_PING', 'value': 62.35},
                          {'timestamp': '2022-04-16 08:35:52.410478', 'device_name': 'VM Lit SL NMS', 'value': 63.77},
                          {'timestamp': '2022-04-16 08:37:47.249796', 'device_name': 'VM Lit SL NMS', 'value': 2.95},
                          {'timestamp': '2022-04-16 08:44:47.211976', 'device_name': 'ADVA FSP3000R7', 'value': 0.74},
                          {'timestamp': '2022-04-16 08:48:46.423455', 'device_name': 'VM Lit SL NMS', 'value': 2.22},
                          {'timestamp': '2022-04-16 08:49:46.375500', 'device_name': 'Catalyst 3500XL', 'value': 42.0},
                          {'timestamp': '2022-04-16 08:58:46.389582', 'device_name': 'Catalyst 3500XL', 'value': 30.51},
                          {'timestamp': '2022-04-16 09:07:52.726828', 'device_name': 'GOOGLE_PING', 'value': 69.1},
                          {'timestamp': '2022-04-16 09:14:52.734695', 'device_name': 'Catalyst 3500XL', 'value': 55.16},
                          {'timestamp': '2022-04-16 09:17:46.837179', 'device_name': 'VM Lit SL NMS', 'value': 4.16},
                          {'timestamp': '2022-04-16 09:19:46.406625', 'device_name': 'VM Lit SL NMS', 'value': 6.51},
                          {'timestamp': '2022-04-16 09:27:46.070019', 'device_name': 'GOOGLE_PING', 'value': 22.91},
                          {'timestamp': '2022-04-16 09:54:47.558486', 'device_name': 'VM Lit SL NMS', 'value': 0.44},
                          {'timestamp': '2022-04-16 10:07:52.762290', 'device_name': 'VM Lit SL NMS', 'value': 38.66},
                          {'timestamp': '2022-04-16 10:09:51.284211', 'device_name': 'ADVA FSP3000R7', 'value': 83.44},
                          {'timestamp': '2022-04-16 10:40:52.006646', 'device_name': 'ADVA FSP3000R7', 'value': 18.9},
                          {'timestamp': '2022-04-16 10:40:52.757462', 'device_name': 'VM Lit SL NMS', 'value': 88.18},
                          {'timestamp': '2022-04-16 10:58:46.384895', 'device_name': 'Ubiquiti OLT', 'value': 2.06},
                          {'timestamp': '2022-04-16 11:00:46.389838', 'device_name': 'ADVA FSP3000R7', 'value': 2.2},
                          {'timestamp': '2022-04-16 11:03:51.582608', 'device_name': 'Ubiquiti OLT', 'value': 83.98},
                          {'timestamp': '2022-04-16 11:18:51.565470', 'device_name': 'ADVA FSP3000R7', 'value': 54.06},
                          {'timestamp': '2022-04-16 11:22:47.564749', 'device_name': 'Ubiquiti OLT', 'value': 33.52},
                          {'timestamp': '2022-04-16 11:36:51.586896', 'device_name': 'GOOGLE_PING', 'value': 39.56},
                          {'timestamp': '2022-04-16 11:41:52.712256', 'device_name': 'Ubiquiti OLT', 'value': 9.99},
                          {'timestamp': '2022-04-16 11:49:46.413342', 'device_name': 'VM Lit SL NMS', 'value': 7.35},
                          {'timestamp': '2022-04-16 11:54:51.297280', 'device_name': 'VM Lit SL NMS', 'value': 62.19},
                          {'timestamp': '2022-04-16 11:56:51.582394', 'device_name': 'Ubiquiti OLT', 'value': 23.71},
                          {'timestamp': '2022-04-16 12:05:51.605892', 'device_name': 'ADVA FSP3000R7', 'value': 25.5},
                          {'timestamp': '2022-04-16 12:35:46.101564', 'device_name': 'VM Lit SL NMS', 'value': 5.13},
                          {'timestamp': '2022-04-16 12:38:46.418739', 'device_name': 'VM Lit SL NMS', 'value': 10.8},
                          {'timestamp': '2022-04-16 12:45:47.528428', 'device_name': 'Ubiquiti OLT', 'value': 14.09},
                          {'timestamp': '2022-04-16 12:51:46.738342', 'device_name': 'ADVA FSP3000R7', 'value': 3.95},
                          {'timestamp': '2022-04-16 12:53:46.064654', 'device_name': 'Catalyst 3500XL', 'value': 5.7},
                          {'timestamp': '2022-04-16 13:01:51.283089', 'device_name': 'Catalyst 3500XL', 'value': 70.93},
                          {'timestamp': '2022-04-16 13:18:46.391552', 'device_name': 'Catalyst 3500XL', 'value': 38.38},
                          {'timestamp': '2022-04-16 13:18:51.305156', 'device_name': 'ADVA FSP3000R7', 'value': 27.62},
                          {'timestamp': '2022-04-16 13:27:51.596831', 'device_name': 'Ubiquiti OLT', 'value': 70.78},
                          {'timestamp': '2022-04-16 13:39:47.550564', 'device_name': 'ADVA FSP3000R7', 'value': 3.83},
                          {'timestamp': '2022-04-16 13:57:47.220822', 'device_name': 'GOOGLE_PING', 'value': 10.03},
                          {'timestamp': '2022-04-16 14:00:52.743862', 'device_name': 'VM Lit SL NMS', 'value': 65.07},
                          {'timestamp': '2022-04-16 14:10:51.579762', 'device_name': 'ADVA FSP3000R7', 'value': 31.63},
                          {'timestamp': '2022-04-16 14:12:46.411285', 'device_name': 'ADVA FSP3000R7', 'value': 1.93},
                          {'timestamp': '2022-04-16 14:14:46.733533', 'device_name': 'VM Lit SL NMS', 'value': 4.02},
                          {'timestamp': '2022-04-16 14:19:51.990876', 'device_name': 'Ubiquiti OLT', 'value': 3.52},
                          {'timestamp': '2022-04-16 14:26:52.379136', 'device_name': 'GOOGLE_PING', 'value': 47.3},
                          {'timestamp': '2022-04-16 15:12:51.594949', 'device_name': 'Ubiquiti OLT', 'value': 91.31},
                          {'timestamp': '2022-04-16 15:22:46.096679', 'device_name': 'Ubiquiti OLT', 'value': 5.54},
                          {'timestamp': '2022-04-16 15:26:47.209487', 'device_name': 'ADVA FSP3000R7', 'value': 3.36},
                          {'timestamp': '2022-04-16 15:42:51.987901', 'device_name': 'Catalyst 3500XL', 'value': 82.71},
                          {'timestamp': '2022-04-16 15:47:52.430305', 'device_name': 'ADVA FSP3000R7', 'value': 40.8},
                          {'timestamp': '2022-04-16 15:59:47.233591', 'device_name': 'ADVA FSP3000R7', 'value': 2.14},
                          {'timestamp': '2022-04-16 15:59:52.750590', 'device_name': 'Catalyst 3500XL', 'value': 7.76},
                          {'timestamp': '2022-04-16 16:12:52.398129', 'device_name': 'VM Lit SL NMS', 'value': 19.75},
                          {'timestamp': '2022-04-16 16:13:52.015735', 'device_name': 'ADVA FSP3000R7', 'value': 89.14},
                          {'timestamp': '2022-04-16 16:23:51.294720', 'device_name': 'Ubiquiti OLT', 'value': 38.68},
                          {'timestamp': '2022-04-16 16:24:47.211497', 'device_name': 'GOOGLE_PING', 'value': 11.77},
                          {'timestamp': '2022-04-16 16:35:51.279387', 'device_name': 'Ubiquiti OLT', 'value': 33.49},
                          {'timestamp': '2022-04-16 16:49:51.301486', 'device_name': 'ADVA FSP3000R7', 'value': 49.54},
                          {'timestamp': '2022-04-16 17:29:51.289158', 'device_name': 'GOOGLE_PING', 'value': 8.12},
                          {'timestamp': '2022-04-16 17:43:46.047132', 'device_name': 'ADVA FSP3000R7', 'value': 3.8},
                          {'timestamp': '2022-04-16 18:00:52.398634', 'device_name': 'GOOGLE_PING', 'value': 14.91},
                          {'timestamp': '2022-04-16 18:09:51.978946', 'device_name': 'Ubiquiti OLT', 'value': 10.43},
                          {'timestamp': '2022-04-16 18:12:52.398607', 'device_name': 'GOOGLE_PING', 'value': 75.9},
                          {'timestamp': '2022-04-16 18:19:46.773887', 'device_name': 'ADVA FSP3000R7', 'value': 1.18},
                          {'timestamp': '2022-04-16 18:27:47.550771', 'device_name': 'Ubiquiti OLT', 'value': 26.53},
                          {'timestamp': '2022-04-16 18:38:52.757841', 'device_name': 'Catalyst 3500XL', 'value': 88.31},
                          {'timestamp': '2022-04-16 18:52:46.397543', 'device_name': 'ADVA FSP3000R7', 'value': 3.86},
                          {'timestamp': '2022-04-16 19:11:46.820956', 'device_name': 'Catalyst 3500XL', 'value': 32.14},
                          {'timestamp': '2022-04-16 19:14:51.300432', 'device_name': 'Ubiquiti OLT', 'value': 62.91},
                          {'timestamp': '2022-04-16 19:17:51.985845', 'device_name': 'Ubiquiti OLT', 'value': 49.97},
                          {'timestamp': '2022-04-16 19:35:51.596377', 'device_name': 'GOOGLE_PING', 'value': 16.67},
                          {'timestamp': '2022-04-16 19:49:52.012942', 'device_name': 'ADVA FSP3000R7', 'value': 94.27},
                          {'timestamp': '2022-04-16 20:00:52.730816', 'device_name': 'Catalyst 3500XL', 'value': 46.27},
                          {'timestamp': '2022-04-16 20:05:51.590898', 'device_name': 'Catalyst 3500XL', 'value': 82.26},
                          {'timestamp': '2022-04-16 20:09:52.725939', 'device_name': 'Catalyst 3500XL', 'value': 20.97},
                          {'timestamp': '2022-04-16 20:33:46.370019', 'device_name': 'Ubiquiti OLT', 'value': 26.56}]

    def test_period_1day(self):
        """
        SELECT
            parentelement, min(value), avg(value)::float(6), max(value), sum(value)::float(6), count(value)
        FROM
            ping_sensor
        WHERE
            period(day, 1, '2022-12-31 00:00:00', timestamp)
        GROUP BY
            parentelement
        """
        query = (self.base_query + ' "SELECT timestamp, parentelement, value FROM ping_sensor '
                 + 'WHERE period(day, 1, \'2022-12-31 00:00:00\', timestamp) ORDER BY timestamp"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'timestamp': '2022-04-15 20:36:51.611916', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 31.68},
                          {'timestamp': '2022-04-15 20:49:51.983142', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 74.33},
                          {'timestamp': '2022-04-15 20:51:51.949947', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 82.0},
                          {'timestamp': '2022-04-15 21:05:46.091270', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 32.33},
                          {'timestamp': '2022-04-15 21:12:46.099052', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.85},
                          {'timestamp': '2022-04-15 21:17:52.737546', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.23},
                          {'timestamp': '2022-04-15 22:00:46.739833', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 37.57},
                          {'timestamp': '2022-04-15 22:01:47.518903', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 19.82},
                          {'timestamp': '2022-04-15 22:03:52.722522', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 17.58},
                          {'timestamp': '2022-04-15 22:09:47.198635', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 33.62},
                          {'timestamp': '2022-04-15 22:18:47.208777', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 6.86},
                          {'timestamp': '2022-04-15 22:37:47.197696', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.73},
                          {'timestamp': '2022-04-15 22:45:46.053343', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 9.59},
                          {'timestamp': '2022-04-15 23:01:51.275600', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 15.4},
                          {'timestamp': '2022-04-15 23:03:46.793179', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.13},
                          {'timestamp': '2022-04-15 23:07:51.991651', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 73.65},
                          {'timestamp': '2022-04-15 23:19:47.546767', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.16},
                          {'timestamp': '2022-04-16 00:00:47.538838', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.88},
                          {'timestamp': '2022-04-16 00:01:52.709776', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 24.02},
                          {'timestamp': '2022-04-16 00:03:47.231798', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 7.49},
                          {'timestamp': '2022-04-16 00:04:46.747923', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 7.73},
                          {'timestamp': '2022-04-16 00:17:52.003149', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 45.38},
                          {'timestamp': '2022-04-16 00:28:46.077640', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 29.78},
                          {'timestamp': '2022-04-16 00:42:47.564284', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 14.54},
                          {'timestamp': '2022-04-16 00:43:52.392446', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 65.37},
                          {'timestamp': '2022-04-16 00:56:51.958241', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 47.22},
                          {'timestamp': '2022-04-16 01:02:46.749881', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.91},
                          {'timestamp': '2022-04-16 01:39:46.411632', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 25.09},
                          {'timestamp': '2022-04-16 01:57:51.256686', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 50.7},
                          {'timestamp': '2022-04-16 02:00:51.262360', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 24.05},
                          {'timestamp': '2022-04-16 02:16:47.240232', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 27.53},
                          {'timestamp': '2022-04-16 02:28:46.751069', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 31.91},
                          {'timestamp': '2022-04-16 02:40:51.596942', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 47.44},
                          {'timestamp': '2022-04-16 03:18:52.372362', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 58.32},
                          {'timestamp': '2022-04-16 03:37:52.755165', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 71.33},
                          {'timestamp': '2022-04-16 03:38:52.378213', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 81.63},
                          {'timestamp': '2022-04-16 03:39:51.996240', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.36},
                          {'timestamp': '2022-04-16 03:40:52.420064', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 59.55},
                          {'timestamp': '2022-04-16 03:43:47.209345', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 30.81},
                          {'timestamp': '2022-04-16 03:48:47.506544', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 20.67},
                          {'timestamp': '2022-04-16 03:50:51.259888', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 43.66},
                          {'timestamp': '2022-04-16 03:53:51.281748', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 84.87},
                          {'timestamp': '2022-04-16 03:57:46.072604', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.96},
                          {'timestamp': '2022-04-16 03:58:52.757976', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 5.14},
                          {'timestamp': '2022-04-16 04:07:46.086082', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 28.38},
                          {'timestamp': '2022-04-16 04:13:46.102537', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.22},
                          {'timestamp': '2022-04-16 04:20:46.841042', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 30.02},
                          {'timestamp': '2022-04-16 04:24:51.580663', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 4.84},
                          {'timestamp': '2022-04-16 04:29:52.738159', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 69.11},
                          {'timestamp': '2022-04-16 04:31:46.085824', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 5.89},
                          {'timestamp': '2022-04-16 04:44:47.523380', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 18.17},
                          {'timestamp': '2022-04-16 04:48:52.734452', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 37.73},
                          {'timestamp': '2022-04-16 04:58:51.994563', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 10.87},
                          {'timestamp': '2022-04-16 05:01:51.985316', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 28.11},
                          {'timestamp': '2022-04-16 05:04:47.203074', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.44},
                          {'timestamp': '2022-04-16 05:05:46.055077', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.31},
                          {'timestamp': '2022-04-16 05:08:46.091144', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.19},
                          {'timestamp': '2022-04-16 05:31:51.981210', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 24.03},
                          {'timestamp': '2022-04-16 05:37:47.536379', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 10.23},
                          {'timestamp': '2022-04-16 05:40:51.253397', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 69.17},
                          {'timestamp': '2022-04-16 05:47:46.063134', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 37.74},
                          {'timestamp': '2022-04-16 05:59:47.249159', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.44},
                          {'timestamp': '2022-04-16 06:20:52.008262', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 43.42},
                          {'timestamp': '2022-04-16 06:21:51.297645', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 44.64},
                          {'timestamp': '2022-04-16 06:24:46.424086', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.03},
                          {'timestamp': '2022-04-16 06:25:51.962046', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 7.85},
                          {'timestamp': '2022-04-16 06:25:52.415621', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 95.05},
                          {'timestamp': '2022-04-16 06:31:51.295456', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 52.6},
                          {'timestamp': '2022-04-16 06:35:52.748065', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 64.32},
                          {'timestamp': '2022-04-16 06:36:46.369390', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.92},
                          {'timestamp': '2022-04-16 06:37:51.587511', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 85.96},
                          {'timestamp': '2022-04-16 06:47:51.297060', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 68.71},
                          {'timestamp': '2022-04-16 06:52:51.957245', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 17.7},
                          {'timestamp': '2022-04-16 06:58:46.056981', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 23.91},
                          {'timestamp': '2022-04-16 07:10:46.088811', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.8},
                          {'timestamp': '2022-04-16 07:11:52.757652', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 31.6},
                          {'timestamp': '2022-04-16 07:20:52.419337', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 84.21},
                          {'timestamp': '2022-04-16 07:28:46.375330', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 0.03},
                          {'timestamp': '2022-04-16 08:15:52.005058', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 89.23},
                          {'timestamp': '2022-04-16 08:20:51.279696', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 33.61},
                          {'timestamp': '2022-04-16 08:21:47.550681', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 32.59},
                          {'timestamp': '2022-04-16 08:35:51.290166', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 62.35},
                          {'timestamp': '2022-04-16 08:35:52.410478', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 63.77},
                          {'timestamp': '2022-04-16 08:37:47.249796', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 2.95},
                          {'timestamp': '2022-04-16 08:44:47.211976', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.74},
                          {'timestamp': '2022-04-16 08:48:46.423455', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 2.22},
                          {'timestamp': '2022-04-16 08:49:46.375500', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 42.0},
                          {'timestamp': '2022-04-16 08:58:46.389582', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 30.51},
                          {'timestamp': '2022-04-16 09:07:52.726828', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 69.1},
                          {'timestamp': '2022-04-16 09:14:52.734695', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 55.16},
                          {'timestamp': '2022-04-16 09:17:46.837179', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 4.16},
                          {'timestamp': '2022-04-16 09:19:46.406625', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 6.51},
                          {'timestamp': '2022-04-16 09:27:46.070019', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 22.91},
                          {'timestamp': '2022-04-16 09:54:47.558486', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 0.44},
                          {'timestamp': '2022-04-16 10:07:52.762290', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 38.66},
                          {'timestamp': '2022-04-16 10:09:51.284211', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 83.44},
                          {'timestamp': '2022-04-16 10:40:52.006646', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 18.9},
                          {'timestamp': '2022-04-16 10:40:52.757462', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 88.18},
                          {'timestamp': '2022-04-16 10:58:46.384895', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 2.06},
                          {'timestamp': '2022-04-16 11:00:46.389838', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.2},
                          {'timestamp': '2022-04-16 11:03:51.582608', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 83.98},
                          {'timestamp': '2022-04-16 11:18:51.565470', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 54.06},
                          {'timestamp': '2022-04-16 11:22:47.564749', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 33.52},
                          {'timestamp': '2022-04-16 11:36:51.586896', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 39.56},
                          {'timestamp': '2022-04-16 11:41:52.712256', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 9.99},
                          {'timestamp': '2022-04-16 11:49:46.413342', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 7.35},
                          {'timestamp': '2022-04-16 11:54:51.297280', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 62.19},
                          {'timestamp': '2022-04-16 11:56:51.582394', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 23.71},
                          {'timestamp': '2022-04-16 12:05:51.605892', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 25.5},
                          {'timestamp': '2022-04-16 12:35:46.101564', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 5.13},
                          {'timestamp': '2022-04-16 12:38:46.418739', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.8},
                          {'timestamp': '2022-04-16 12:45:47.528428', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 14.09},
                          {'timestamp': '2022-04-16 12:51:46.738342', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.95},
                          {'timestamp': '2022-04-16 12:53:46.064654', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 5.7},
                          {'timestamp': '2022-04-16 13:01:51.283089', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 70.93},
                          {'timestamp': '2022-04-16 13:18:46.391552', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 38.38},
                          {'timestamp': '2022-04-16 13:18:51.305156', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 27.62},
                          {'timestamp': '2022-04-16 13:27:51.596831', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 70.78},
                          {'timestamp': '2022-04-16 13:39:47.550564', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.83},
                          {'timestamp': '2022-04-16 13:57:47.220822', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 10.03},
                          {'timestamp': '2022-04-16 14:00:52.743862', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 65.07},
                          {'timestamp': '2022-04-16 14:10:51.579762', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 31.63},
                          {'timestamp': '2022-04-16 14:12:46.411285', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.93},
                          {'timestamp': '2022-04-16 14:14:46.733533', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 4.02},
                          {'timestamp': '2022-04-16 14:19:51.990876', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 3.52},
                          {'timestamp': '2022-04-16 14:26:52.379136', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 47.3},
                          {'timestamp': '2022-04-16 15:12:51.594949', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 91.31},
                          {'timestamp': '2022-04-16 15:22:46.096679', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 5.54},
                          {'timestamp': '2022-04-16 15:26:47.209487', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.36},
                          {'timestamp': '2022-04-16 15:42:51.987901', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 82.71},
                          {'timestamp': '2022-04-16 15:47:52.430305', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 40.8},
                          {'timestamp': '2022-04-16 15:59:47.233591', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.14},
                          {'timestamp': '2022-04-16 15:59:52.750590', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 7.76},
                          {'timestamp': '2022-04-16 16:12:52.398129', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 19.75},
                          {'timestamp': '2022-04-16 16:13:52.015735', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 89.14},
                          {'timestamp': '2022-04-16 16:23:51.294720', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 38.68},
                          {'timestamp': '2022-04-16 16:24:47.211497', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 11.77},
                          {'timestamp': '2022-04-16 16:35:51.279387', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 33.49},
                          {'timestamp': '2022-04-16 16:49:51.301486', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 49.54},
                          {'timestamp': '2022-04-16 17:29:51.289158', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 8.12},
                          {'timestamp': '2022-04-16 17:43:46.047132', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.8},
                          {'timestamp': '2022-04-16 18:00:52.398634', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.91},
                          {'timestamp': '2022-04-16 18:09:51.978946', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 10.43},
                          {'timestamp': '2022-04-16 18:12:52.398607', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 75.9},
                          {'timestamp': '2022-04-16 18:19:46.773887', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.18},
                          {'timestamp': '2022-04-16 18:27:47.550771', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.53},
                          {'timestamp': '2022-04-16 18:38:52.757841', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 88.31},
                          {'timestamp': '2022-04-16 18:52:46.397543', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.86},
                          {'timestamp': '2022-04-16 19:11:46.820956', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 32.14},
                          {'timestamp': '2022-04-16 19:14:51.300432', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 62.91},
                          {'timestamp': '2022-04-16 19:17:51.985845', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 49.97},
                          {'timestamp': '2022-04-16 19:35:51.596377', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 16.67},
                          {'timestamp': '2022-04-16 19:49:52.012942', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 94.27},
                          {'timestamp': '2022-04-16 20:00:52.730816', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 46.27},
                          {'timestamp': '2022-04-16 20:05:51.590898', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 82.26},
                          {'timestamp': '2022-04-16 20:09:52.725939', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 20.97},
                          {'timestamp': '2022-04-16 20:33:46.370019', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.56}]

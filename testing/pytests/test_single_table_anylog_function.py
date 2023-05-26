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
        cls.base_query = f"sql test format=json and stat=false "

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

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_val': 0.0, 'avg_val': 1.962685, 'max_val': 3.99, 'sum_val': 635.91, 'row_count': 324},
                          {'device_name': 'Catalyst 3500XL', 'min_val': 0.46, 'avg_val': 25.286921, 'max_val': 48.97, 'sum_val': 7636.65, 'row_count': 302},
                          {'device_name': 'GOOGLE_PING', 'min_val': 2.09, 'avg_val': 19.795886, 'max_val': 36.95, 'sum_val': 6592.03, 'row_count': 333},
                          {'device_name': 'Ubiquiti OLT', 'min_val': 0.11, 'avg_val': 25.653353, 'max_val': 48.63, 'sum_val': 8491.26, 'row_count': 331},
                          {'device_name': 'VM Lit SL NMS', 'min_val': 0.01, 'avg_val': 5.387875, 'max_val': 10.95, 'sum_val': 1901.92, 'row_count': 353}]

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

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_val': 0.0, 'avg_val': 1.962685, 'max_val': 3.99, 'sum_val': 635.91, 'row_count': 324},
                          {'device_name': 'Catalyst 3500XL', 'min_val': 0.46, 'avg_val': 25.286921, 'max_val': 48.97, 'sum_val': 7636.65, 'row_count': 302},
                          {'device_name': 'GOOGLE_PING', 'min_val': 2.09, 'avg_val': 19.795886, 'max_val': 36.95, 'sum_val': 6592.03, 'row_count': 333},
                          {'device_name': 'Ubiquiti OLT', 'min_val': 0.11, 'avg_val': 25.653353, 'max_val': 48.63, 'sum_val': 8491.26, 'row_count': 331},
                          {'device_name': 'VM Lit SL NMS', 'min_val': 0.01, 'avg_val': 5.387875, 'max_val': 10.95, 'sum_val': 1901.92, 'row_count': 353}]

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

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 5.387875, 'max_val': 10.95, 'sum_val': 1901.92, 'row_count': 353},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 1.962685, 'max_val': 3.99, 'sum_val': 635.91, 'row_count': 324},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 25.286921, 'max_val': 48.97, 'sum_val': 7636.65, 'row_count': 302},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 25.653353, 'max_val': 48.63, 'sum_val': 8491.26, 'row_count': 331},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 2.09, 'avg_val': 19.795886, 'max_val': 36.95, 'sum_val': 6592.03, 'row_count': 333}]

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

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 5.387875, 'max_val': 10.95, 'sum_val': 1901.92, 'row_count': 353},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 1.962685, 'max_val': 3.99, 'sum_val': 635.91, 'row_count': 324},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 25.286921, 'max_val': 48.97, 'sum_val': 7636.65, 'row_count': 302},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 25.653353, 'max_val': 48.63, 'sum_val': 8491.26, 'row_count': 331},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 2.09, 'avg_val': 19.795886, 'max_val': 36.95, 'sum_val': 6592.03, 'row_count': 333}]

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

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_val': 0.01, 'avg_val': 5.387875, 'max_val': 10.95, 'sum_val': 1901.92, 'row_count': 353},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 0.0, 'avg_val': 1.962685, 'max_val': 3.99, 'sum_val': 635.91, 'row_count': 324},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 0.46, 'avg_val': 25.286921, 'max_val': 48.97, 'sum_val': 7636.65, 'row_count': 302},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 0.11, 'avg_val': 25.653353, 'max_val': 48.63, 'sum_val': 8491.26, 'row_count': 331},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 2.09, 'avg_val': 19.795886, 'max_val': 36.95, 'sum_val': 6592.03, 'row_count': 333}]

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

        assert result == [{'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_val': 1.18, 'avg_val': 2.868, 'max_val': 3.86, 'sum_val': 14.34, 'row_count': 5},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_val': 32.14, 'avg_val': 32.14, 'max_val': 32.14, 'sum_val': 32.14, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_val': 5.54, 'avg_val': 19.543333, 'max_val': 26.56, 'sum_val': 58.63, 'row_count': 3},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_val': 11.77, 'avg_val': 11.77, 'max_val': 11.77, 'sum_val': 11.77, 'row_count': 1}]

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

        assert result == [{'timestamp': '2022-04-16 08:37:47.249796', 'device_name': 'VM Lit SL NMS', 'value': 2.95},
                          {'timestamp': '2022-04-16 08:44:47.211976', 'device_name': 'ADVA FSP3000R7', 'value': 0.74},
                          {'timestamp': '2022-04-16 08:48:46.423455', 'device_name': 'VM Lit SL NMS', 'value': 2.22},
                          {'timestamp': '2022-04-16 08:49:46.375500', 'device_name': 'Catalyst 3500XL', 'value': 42.0},
                          {'timestamp': '2022-04-16 08:58:46.389582', 'device_name': 'Catalyst 3500XL', 'value': 30.51},
                          {'timestamp': '2022-04-16 09:17:46.837179', 'device_name': 'VM Lit SL NMS', 'value': 4.16},
                          {'timestamp': '2022-04-16 09:19:46.406625', 'device_name': 'VM Lit SL NMS', 'value': 6.51},
                          {'timestamp': '2022-04-16 09:27:46.070019', 'device_name': 'GOOGLE_PING', 'value': 22.91},
                          {'timestamp': '2022-04-16 09:54:47.558486', 'device_name': 'VM Lit SL NMS', 'value': 0.44},
                          {'timestamp': '2022-04-16 10:58:46.384895', 'device_name': 'Ubiquiti OLT', 'value': 2.06},
                          {'timestamp': '2022-04-16 11:00:46.389838', 'device_name': 'ADVA FSP3000R7', 'value': 2.2},
                          {'timestamp': '2022-04-16 11:22:47.564749', 'device_name': 'Ubiquiti OLT', 'value': 33.52},
                          {'timestamp': '2022-04-16 11:49:46.413342', 'device_name': 'VM Lit SL NMS', 'value': 7.35},
                          {'timestamp': '2022-04-16 12:35:46.101564', 'device_name': 'VM Lit SL NMS', 'value': 5.13},
                          {'timestamp': '2022-04-16 12:38:46.418739', 'device_name': 'VM Lit SL NMS', 'value': 10.8},
                          {'timestamp': '2022-04-16 12:45:47.528428', 'device_name': 'Ubiquiti OLT', 'value': 14.09},
                          {'timestamp': '2022-04-16 12:51:46.738342', 'device_name': 'ADVA FSP3000R7', 'value': 3.95},
                          {'timestamp': '2022-04-16 12:53:46.064654', 'device_name': 'Catalyst 3500XL', 'value': 5.7},
                          {'timestamp': '2022-04-16 13:18:46.391552', 'device_name': 'Catalyst 3500XL', 'value': 38.38},
                          {'timestamp': '2022-04-16 13:39:47.550564', 'device_name': 'ADVA FSP3000R7', 'value': 3.83},
                          {'timestamp': '2022-04-16 13:57:47.220822', 'device_name': 'GOOGLE_PING', 'value': 10.03},
                          {'timestamp': '2022-04-16 14:12:46.411285', 'device_name': 'ADVA FSP3000R7', 'value': 1.93},
                          {'timestamp': '2022-04-16 14:14:46.733533', 'device_name': 'VM Lit SL NMS', 'value': 4.02},
                          {'timestamp': '2022-04-16 15:22:46.096679', 'device_name': 'Ubiquiti OLT', 'value': 5.54},
                          {'timestamp': '2022-04-16 15:26:47.209487', 'device_name': 'ADVA FSP3000R7', 'value': 3.36},
                          {'timestamp': '2022-04-16 15:59:47.233591', 'device_name': 'ADVA FSP3000R7', 'value': 2.14},
                          {'timestamp': '2022-04-16 16:24:47.211497', 'device_name': 'GOOGLE_PING', 'value': 11.77},
                          {'timestamp': '2022-04-16 17:43:46.047132', 'device_name': 'ADVA FSP3000R7', 'value': 3.8},
                          {'timestamp': '2022-04-16 18:19:46.773887', 'device_name': 'ADVA FSP3000R7', 'value': 1.18},
                          {'timestamp': '2022-04-16 18:27:47.550771', 'device_name': 'Ubiquiti OLT', 'value': 26.53},
                          {'timestamp': '2022-04-16 18:52:46.397543', 'device_name': 'ADVA FSP3000R7', 'value': 3.86},
                          {'timestamp': '2022-04-16 19:11:46.820956', 'device_name': 'Catalyst 3500XL', 'value': 32.14},
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

        assert result == [{'timestamp': '2022-04-15 21:05:46.091270', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 32.33},
                          {'timestamp': '2022-04-15 21:12:46.099052', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.85},
                          {'timestamp': '2022-04-15 22:00:46.739833', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 37.57},
                          {'timestamp': '2022-04-15 22:01:47.518903', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 19.82},
                          {'timestamp': '2022-04-15 22:09:47.198635', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 33.62},
                          {'timestamp': '2022-04-15 22:18:47.208777', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 6.86},
                          {'timestamp': '2022-04-15 22:37:47.197696', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.73},
                          {'timestamp': '2022-04-15 22:45:46.053343', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 9.59},
                          {'timestamp': '2022-04-15 23:03:46.793179', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.13},
                          {'timestamp': '2022-04-15 23:19:47.546767', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.16},
                          {'timestamp': '2022-04-16 00:00:47.538838', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.88},
                          {'timestamp': '2022-04-16 00:03:47.231798', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 7.49},
                          {'timestamp': '2022-04-16 00:04:46.747923', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 7.73},
                          {'timestamp': '2022-04-16 00:28:46.077640', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 29.78},
                          {'timestamp': '2022-04-16 00:42:47.564284', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 14.54},
                          {'timestamp': '2022-04-16 01:02:46.749881', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.91},
                          {'timestamp': '2022-04-16 01:39:46.411632', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 25.09},
                          {'timestamp': '2022-04-16 02:16:47.240232', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 27.53},
                          {'timestamp': '2022-04-16 02:28:46.751069', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 31.91},
                          {'timestamp': '2022-04-16 03:43:47.209345', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 30.81}, 
                          {'timestamp': '2022-04-16 03:48:47.506544', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 20.67},
                          {'timestamp': '2022-04-16 03:57:46.072604', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.96},
                          {'timestamp': '2022-04-16 04:07:46.086082', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 28.38}, 
                          {'timestamp': '2022-04-16 04:13:46.102537', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 14.22}, 
                          {'timestamp': '2022-04-16 04:20:46.841042', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 30.02}, 
                          {'timestamp': '2022-04-16 04:31:46.085824', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 5.89},
                          {'timestamp': '2022-04-16 04:44:47.523380', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 18.17}, 
                          {'timestamp': '2022-04-16 05:04:47.203074', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.44}, 
                          {'timestamp': '2022-04-16 05:05:46.055077', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.31},
                          {'timestamp': '2022-04-16 05:08:46.091144', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.19}, 
                          {'timestamp': '2022-04-16 05:37:47.536379', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 10.23},
                          {'timestamp': '2022-04-16 05:47:46.063134', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 37.74},
                          {'timestamp': '2022-04-16 05:59:47.249159', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.44}, 
                          {'timestamp': '2022-04-16 06:24:46.424086', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.03},
                          {'timestamp': '2022-04-16 06:36:46.369390', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.92}, 
                          {'timestamp': '2022-04-16 06:58:46.056981', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 23.91},
                          {'timestamp': '2022-04-16 07:10:46.088811', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.8}, 
                          {'timestamp': '2022-04-16 07:28:46.375330', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 0.03}, 
                          {'timestamp': '2022-04-16 08:21:47.550681', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 32.59},
                          {'timestamp': '2022-04-16 08:37:47.249796', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 2.95}, 
                          {'timestamp': '2022-04-16 08:44:47.211976', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 0.74},
                          {'timestamp': '2022-04-16 08:48:46.423455', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 2.22},
                          {'timestamp': '2022-04-16 08:49:46.375500', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 42.0},
                          {'timestamp': '2022-04-16 08:58:46.389582', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 30.51},
                          {'timestamp': '2022-04-16 09:17:46.837179', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 4.16},
                          {'timestamp': '2022-04-16 09:19:46.406625', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 6.51},
                          {'timestamp': '2022-04-16 09:27:46.070019', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 22.91},
                          {'timestamp': '2022-04-16 09:54:47.558486', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 0.44}, 
                          {'timestamp': '2022-04-16 10:58:46.384895', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 2.06}, 
                          {'timestamp': '2022-04-16 11:00:46.389838', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.2},
                          {'timestamp': '2022-04-16 11:22:47.564749', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 33.52},
                          {'timestamp': '2022-04-16 11:49:46.413342', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 7.35}, 
                          {'timestamp': '2022-04-16 12:35:46.101564', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 5.13}, 
                          {'timestamp': '2022-04-16 12:38:46.418739', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 10.8},
                          {'timestamp': '2022-04-16 12:45:47.528428', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 14.09}, 
                          {'timestamp': '2022-04-16 12:51:46.738342', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.95},
                          {'timestamp': '2022-04-16 12:53:46.064654', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 5.7},
                          {'timestamp': '2022-04-16 13:18:46.391552', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 38.38},
                          {'timestamp': '2022-04-16 13:39:47.550564', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.83},
                          {'timestamp': '2022-04-16 13:57:47.220822', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 10.03},
                          {'timestamp': '2022-04-16 14:12:46.411285', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.93},
                          {'timestamp': '2022-04-16 14:14:46.733533', 'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'value': 4.02},
                          {'timestamp': '2022-04-16 15:22:46.096679', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 5.54},
                          {'timestamp': '2022-04-16 15:26:47.209487', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.36},
                          {'timestamp': '2022-04-16 15:59:47.233591', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 2.14},
                          {'timestamp': '2022-04-16 16:24:47.211497', 'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'value': 11.77},
                          {'timestamp': '2022-04-16 17:43:46.047132', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.8},
                          {'timestamp': '2022-04-16 18:19:46.773887', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 1.18},
                          {'timestamp': '2022-04-16 18:27:47.550771', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.53},
                          {'timestamp': '2022-04-16 18:52:46.397543', 'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'value': 3.86},
                          {'timestamp': '2022-04-16 19:11:46.820956', 'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'value': 32.14},
                          {'timestamp': '2022-04-16 20:33:46.370019', 'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'value': 26.56}]

    def test_increments_1month(self):
        query = (self.base_query + ' "SELECT increments(month, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\'"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.896316, 'max_val': 49.0, 'sum_val': 31888.01, 'row_count': 2006},
                          {'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.0, 'avg_val': 14.877294, 'max_val': 48.98, 'sum_val': 62945.83, 'row_count': 4231},
                          {'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.01, 'avg_val': 15.118887, 'max_val': 49.0, 'sum_val': 32052.04, 'row_count': 2120}]

    def test_increments_30day(self):
        query = (self.base_query + ' "SELECT increments(day, 30, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\' GROUP BY device_name;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-13 21:21:47.231712', 'max_ts': '2022-02-28 23:34:46.063492', 'min_val': 0.0, 'avg_val': 1.942392, 'max_val': 3.99, 'sum_val': 811.92, 'row_count': 418},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-02-13 21:58:46.378304', 'max_ts': '2022-02-28 22:19:47.209004', 'min_val': 0.09, 'avg_val': 25.677103, 'max_val': 48.96, 'sum_val': 10014.07, 'row_count': 390},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-13 22:09:46.053613', 'max_ts': '2022-02-28 23:39:47.519260', 'min_val': 2.01, 'avg_val': 18.988067, 'max_val': 36.89, 'sum_val': 7956.0, 'row_count': 419},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.05, 'avg_val': 26.580478, 'max_val': 49.0, 'sum_val': 11110.64, 'row_count': 418},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-14 00:05:46.394511', 'max_ts': '2022-02-28 20:07:46.842465', 'min_val': 0.02, 'avg_val': 5.527368, 'max_val': 10.96, 'sum_val': 1995.38, 'row_count': 361},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-01 00:36:46.057636', 'max_ts': '2022-03-29 23:16:47.526701', 'min_val': 0.0, 'avg_val': 1.950225, 'max_val': 4.0, 'sum_val': 1558.23, 'row_count': 799},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-01 00:30:46.096552', 'max_ts': '2022-03-29 19:04:46.743505', 'min_val': 0.03, 'avg_val': 23.650424, 'max_val': 48.93, 'sum_val': 19511.6, 'row_count': 825},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-29 23:14:47.514567', 'min_val': 2.02, 'avg_val': 19.268471, 'max_val': 36.99, 'sum_val': 14239.4, 'row_count': 739},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-01 00:07:46.084507', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.19, 'avg_val': 24.523037, 'max_val': 48.98, 'sum_val': 19299.63, 'row_count': 787},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-01 00:05:46.393130', 'max_ts': '2022-03-29 23:38:47.226700', 'min_val': 0.0, 'avg_val': 5.484829, 'max_val': 11.0, 'sum_val': 4486.59, 'row_count': 818},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 1.885965, 'max_val': 4.0, 'sum_val': 107.5, 'row_count': 57},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-30 00:45:46.761087', 'max_ts': '2022-03-31 22:20:46.755617', 'min_val': 0.61, 'avg_val': 22.431176, 'max_val': 48.87, 'sum_val': 1143.99, 'row_count': 51},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-30 00:24:47.203820', 'max_ts': '2022-03-31 22:33:46.377127', 'min_val': 2.06, 'avg_val': 19.812121, 'max_val': 36.85, 'sum_val': 1307.6, 'row_count': 66},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-30 00:29:46.732619', 'max_ts': '2022-03-31 22:54:46.059694', 'min_val': 0.85, 'avg_val': 21.7176, 'max_val': 47.09, 'sum_val': 1085.88, 'row_count': 50},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-30 01:36:47.522643', 'max_ts': '2022-03-31 21:53:47.540473', 'min_val': 0.14, 'avg_val': 5.266923, 'max_val': 9.66, 'sum_val': 205.41, 'row_count': 39},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-01 00:44:47.225572', 'max_ts': '2022-04-16 18:52:46.397543', 'min_val': 0.01, 'avg_val': 2.056131, 'max_val': 3.97, 'sum_val': 908.81, 'row_count': 442},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-16 19:11:46.820956', 'min_val': 0.17, 'avg_val': 24.587838, 'max_val': 48.63, 'sum_val': 10007.25, 'row_count': 407},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-16 16:24:47.211497', 'min_val': 2.03, 'avg_val': 20.186714, 'max_val': 36.99, 'sum_val': 8478.42, 'row_count': 420},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-01 01:10:46.087993', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.42, 'avg_val': 24.478667, 'max_val': 49.0, 'sum_val': 10281.04, 'row_count': 420},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 14:14:46.733533', 'min_val': 0.03, 'avg_val': 5.513968, 'max_val': 11.0, 'sum_val': 2376.52, 'row_count': 431}]

    def test_increments_15day(self):
        query = (self.base_query + ' "SELECT increments(day, 15, timestamp), parentelement, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-01 00:00:00\' AND timestamp <= \'2022-04-30 23:59:59\' GROUP BY parentelement;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-14 23:17:46.103727', 'min_val': 0.03, 'avg_val': 5.49801, 'max_val': 11.0, 'sum_val': 2155.22, 'row_count': 392},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:44:47.225572', 'max_ts': '2022-04-14 23:35:46.425955', 'min_val': 0.01, 'avg_val': 2.054461, 'max_val': 3.96, 'sum_val': 819.73, 'row_count': 399},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-14 23:04:47.565266', 'min_val': 0.17, 'avg_val': 24.92841, 'max_val': 48.63, 'sum_val': 9248.44, 'row_count': 371},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 01:10:46.087993', 'max_ts': '2022-04-14 23:40:47.530353', 'min_val': 0.42, 'avg_val': 24.659581, 'max_val': 49.0, 'sum_val': 9419.96, 'row_count': 382},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-14 22:52:47.518726', 'min_val': 2.03, 'avg_val': 19.943342, 'max_val': 36.95, 'sum_val': 7638.3, 'row_count': 383},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-16 14:14:46.733533', 'min_val': 0.03, 'avg_val': 5.674359, 'max_val': 10.8, 'sum_val': 221.3, 'row_count': 39},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 01:36:46.410228', 'max_ts': '2022-04-16 18:52:46.397543', 'min_val': 0.04, 'avg_val': 2.071628, 'max_val': 3.97, 'sum_val': 89.08, 'row_count': 43},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-16 19:11:46.820956', 'min_val': 2.94, 'avg_val': 21.078056, 'max_val': 42.83, 'sum_val': 758.81, 'row_count': 36},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 2.06, 'avg_val': 22.66, 'max_val': 46.38, 'sum_val': 861.08, 'row_count': 38},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:56:47.220851', 'max_ts': '2022-04-16 16:24:47.211497', 'min_val': 5.64, 'avg_val': 22.705946, 'max_val': 36.99, 'sum_val': 840.12, 'row_count': 37}]

    #@pytest.mark.skip("Difference in output")
    def test_increments_7day(self):
        query = (self.base_query + ' "SELECT increments(day, 7, timestamp), parentelement, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-01 00:00:00\' AND timestamp <= \'2022-04-30 23:59:59\' GROUP BY parentelement '
                +' ORDER BY parentelement, min_ts ASC;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-06 23:27:47.209429', 'min_val': 0.03, 'avg_val': 5.555438, 'max_val': 11.0, 'sum_val': 888.87, 'row_count': 160},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:44:47.225572', 'max_ts': '2022-04-06 23:58:47.213812', 'min_val': 0.01, 'avg_val': 2.088079, 'max_val': 3.96, 'sum_val': 369.59, 'row_count': 177},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-06 23:39:47.534365', 'min_val': 0.54, 'avg_val': 25.97018, 'max_val': 48.58, 'sum_val': 4337.02, 'row_count': 167},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 01:10:46.087993', 'max_ts': '2022-04-06 23:53:47.221785', 'min_val': 0.42, 'avg_val': 24.627365, 'max_val': 48.82, 'sum_val': 4112.77, 'row_count': 167},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-06 23:12:46.045029', 'min_val': 2.19, 'avg_val': 20.11741, 'max_val': 36.77, 'sum_val': 3339.49, 'row_count': 166},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-07 00:12:47.522063', 'max_ts': '2022-04-13 23:42:46.381817', 'min_val': 0.15, 'avg_val': 5.554952, 'max_val': 10.99, 'sum_val': 1155.43, 'row_count': 208},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-07 01:08:47.241045', 'max_ts': '2022-04-13 22:53:47.533648', 'min_val': 0.02, 'avg_val': 1.966684, 'max_val': 3.93, 'sum_val': 385.47, 'row_count': 196},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-07 00:41:47.228909', 'max_ts': '2022-04-13 23:51:46.079040', 'min_val': 0.17, 'avg_val': 24.159826, 'max_val': 48.63, 'sum_val': 4155.49, 'row_count': 172},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-07 01:09:46.075252', 'max_ts': '2022-04-13 22:58:46.426069', 'min_val': 0.6, 'avg_val': 25.436162, 'max_val': 49.0, 'sum_val': 4705.69, 'row_count': 185},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-07 00:12:47.221580', 'max_ts': '2022-04-13 23:59:47.536930', 'min_val': 2.03, 'avg_val': 20.484762, 'max_val': 36.95, 'sum_val': 3871.62, 'row_count': 189},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-14 00:26:46.079578', 'max_ts': '2022-04-16 14:14:46.733533', 'min_val': 0.03, 'avg_val': 5.273333, 'max_val': 10.8, 'sum_val': 332.22, 'row_count': 63},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-14 00:16:46.103756', 'max_ts': '2022-04-16 18:52:46.397543', 'min_val': 0.04, 'avg_val': 2.228261, 'max_val': 3.97, 'sum_val': 153.75, 'row_count': 69},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-14 00:08:47.210957', 'max_ts': '2022-04-16 19:11:46.820956', 'min_val': 2.24, 'avg_val': 22.275588, 'max_val': 45.33, 'sum_val': 1514.74, 'row_count': 68},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-14 00:43:46.383571', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.67, 'avg_val': 21.508529, 'max_val': 46.38, 'sum_val': 1462.58, 'row_count': 68},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-14 00:00:47.197981', 'max_ts': '2022-04-16 16:24:47.211497', 'min_val': 2.07, 'avg_val': 19.497077, 'max_val': 36.99, 'sum_val': 1267.31, 'row_count': 65}]

    @pytest.mark.skip("Difference in output")
    def test_increments_1day(self):
        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-01 00:00:00\' AND timestamp <= \'2022-04-20 23:59:59\' GROUP BY device_name '
                +' ORDER BY device_name, min_ts ASC;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-01 00:44:47.225572', 'max_ts': '2022-04-01 23:18:47.221957', 'min_val': 0.1, 'avg_val': 2.01375, 'max_val': 3.88, 'sum_val': 64.44, 'row_count': 32},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-01 23:25:46.398127', 'min_val': 2.81, 'avg_val': 23.223214, 'max_val': 47.2, 'sum_val': 650.25, 'row_count': 28},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-01 23:36:46.100232', 'min_val': 3.17, 'avg_val': 18.376, 'max_val': 32.68, 'sum_val': 551.28, 'row_count': 30},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-01 01:10:46.087993', 'max_ts': '2022-04-01 23:15:46.089610', 'min_val': 0.91, 'avg_val': 26.881935, 'max_val': 48.82, 'sum_val': 833.34, 'row_count': 31},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-01 23:55:46.791227', 'min_val': 1.19, 'avg_val': 5.976667, 'max_val': 11.0, 'sum_val': 179.3, 'row_count': 30},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-02 00:18:46.097253', 'max_ts': '2022-04-02 22:13:47.510856', 'min_val': 0.07, 'avg_val': 1.92875, 'max_val': 3.83, 'sum_val': 61.72, 'row_count': 32},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-02 00:04:47.523782', 'max_ts': '2022-04-02 21:57:46.418343', 'min_val': 0.91, 'avg_val': 25.00963, 'max_val': 48.58, 'sum_val': 675.26, 'row_count': 27},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-02 00:56:47.558373', 'max_ts': '2022-04-02 23:19:47.207896', 'min_val': 7.01, 'avg_val': 23.651563, 'max_val': 35.96, 'sum_val': 756.85, 'row_count': 32},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-02 04:19:46.409543', 'max_ts': '2022-04-02 22:24:46.758205', 'min_val': 0.42, 'avg_val': 25.896667, 'max_val': 47.15, 'sum_val': 699.21, 'row_count': 27},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-02 00:23:46.421259', 'max_ts': '2022-04-02 21:29:47.550651', 'min_val': 0.29, 'avg_val': 5.284286, 'max_val': 10.41, 'sum_val': 73.98, 'row_count': 14},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-03 00:08:47.210644', 'max_ts': '2022-04-03 23:55:47.562973', 'min_val': 0.21, 'avg_val': 2.052692, 'max_val': 3.96, 'sum_val': 53.37, 'row_count': 26},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-03 00:00:47.193778', 'max_ts': '2022-04-03 23:26:47.208378', 'min_val': 2.78, 'avg_val': 26.414074, 'max_val': 47.16, 'sum_val': 713.18, 'row_count': 27},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-03 01:11:46.421403', 'max_ts': '2022-04-03 22:10:46.074176', 'min_val': 4.86, 'avg_val': 18.892, 'max_val': 30.85, 'sum_val': 377.84, 'row_count': 20},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-03 01:47:46.378619', 'max_ts': '2022-04-03 23:50:47.547861', 'min_val': 2.01, 'avg_val': 25.925172, 'max_val': 46.66, 'sum_val': 751.83, 'row_count': 29},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-03 00:01:47.517893', 'max_ts': '2022-04-03 22:43:46.382755', 'min_val': 0.03, 'avg_val': 5.711429, 'max_val': 10.78, 'sum_val': 159.92, 'row_count': 28},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-04 00:03:47.245980', 'max_ts': '2022-04-04 23:20:46.743822', 'min_val': 0.01, 'avg_val': 1.75931, 'max_val': 3.86, 'sum_val': 51.02, 'row_count': 29},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-04 00:49:47.533213', 'max_ts': '2022-04-04 23:45:47.509976', 'min_val': 2.85, 'avg_val': 28.094615, 'max_val': 48.21, 'sum_val': 730.46, 'row_count': 26},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-04 00:27:46.370194', 'max_ts': '2022-04-04 23:57:46.812424', 'min_val': 2.19, 'avg_val': 21.5112, 'max_val': 36.63, 'sum_val': 537.78, 'row_count': 25},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-04 00:44:46.821029', 'max_ts': '2022-04-04 22:53:46.816351', 'min_val': 3.11, 'avg_val': 24.512258, 'max_val': 48.09, 'sum_val': 759.88, 'row_count': 31},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-04 00:17:47.543806', 'max_ts': '2022-04-04 22:50:46.793660', 'min_val': 0.24, 'avg_val': 5.828649, 'max_val': 10.76, 'sum_val': 215.66, 'row_count': 37},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-05 00:01:46.386239', 'max_ts': '2022-04-05 23:35:47.231827', 'min_val': 0.09, 'avg_val': 2.275625, 'max_val': 3.8, 'sum_val': 72.82, 'row_count': 32},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-05 00:07:46.075457', 'max_ts': '2022-04-05 23:11:46.755560', 'min_val': 4.06, 'avg_val': 27.948, 'max_val': 48.31, 'sum_val': 698.7, 'row_count': 25},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-05 00:46:47.563412', 'max_ts': '2022-04-05 23:59:47.223935', 'min_val': 2.49, 'avg_val': 19.007407, 'max_val': 36.77, 'sum_val': 513.2, 'row_count': 27},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-05 00:24:46.847927', 'max_ts': '2022-04-05 22:55:47.551902', 'min_val': 2.4, 'avg_val': 23.967143, 'max_val': 47.67, 'sum_val': 671.08, 'row_count': 28},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-05 00:14:47.203792', 'max_ts': '2022-04-05 22:07:47.195756', 'min_val': 0.17, 'avg_val': 4.67125, 'max_val': 10.4, 'sum_val': 112.11, 'row_count': 24},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-06 00:08:46.759124', 'max_ts': '2022-04-06 23:58:47.213812', 'min_val': 1.37, 'avg_val': 2.546923, 'max_val': 3.96, 'sum_val': 66.22, 'row_count': 26},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-06 00:28:47.562915', 'max_ts': '2022-04-06 23:39:47.534365', 'min_val': 0.54, 'avg_val': 25.563824, 'max_val': 47.78, 'sum_val': 869.17, 'row_count': 34},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-06 00:01:46.835344', 'max_ts': '2022-04-06 23:12:46.045029', 'min_val': 2.28, 'avg_val': 18.829375, 'max_val': 35.92, 'sum_val': 602.54, 'row_count': 32},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-06 03:11:46.395344', 'max_ts': '2022-04-06 23:53:47.221785', 'min_val': 1.19, 'avg_val': 18.925238, 'max_val': 46.99, 'sum_val': 397.43, 'row_count': 21},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-06 01:33:47.204866', 'max_ts': '2022-04-06 23:27:47.209429', 'min_val': 0.06, 'avg_val': 5.477778, 'max_val': 10.12, 'sum_val': 147.9, 'row_count': 27},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-07 01:08:47.241045', 'max_ts': '2022-04-07 23:53:46.400902', 'min_val': 0.07, 'avg_val': 1.652727, 'max_val': 3.83, 'sum_val': 36.36, 'row_count': 22},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-07 00:41:47.228909', 'max_ts': '2022-04-07 21:03:46.774468', 'min_val': 1.29, 'avg_val': 26.777333, 'max_val': 48.02, 'sum_val': 803.32, 'row_count': 30},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-07 00:12:47.221580', 'max_ts': '2022-04-07 23:16:46.094864', 'min_val': 8.94, 'avg_val': 20.67, 'max_val': 36.95, 'sum_val': 496.08, 'row_count': 24},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-07 01:09:46.075252', 'max_ts': '2022-04-07 23:46:47.561796', 'min_val': 9.74, 'avg_val': 29.175455, 'max_val': 49.0, 'sum_val': 641.86, 'row_count': 22},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-07 00:12:47.522063', 'max_ts': '2022-04-07 23:54:46.419621', 'min_val': 0.15, 'avg_val': 6.453043, 'max_val': 10.53, 'sum_val': 148.42, 'row_count': 23},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-08 00:24:46.379911', 'max_ts': '2022-04-08 21:40:46.386326', 'min_val': 0.03, 'avg_val': 1.841818, 'max_val': 3.88, 'sum_val': 60.78, 'row_count': 33},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-08 00:58:46.827348', 'max_ts': '2022-04-08 23:58:46.834054', 'min_val': 0.58, 'avg_val': 21.925714, 'max_val': 46.79, 'sum_val': 613.92, 'row_count': 28},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-08 03:02:47.543099', 'max_ts': '2022-04-08 23:36:46.378418', 'min_val': 2.03, 'avg_val': 21.1576, 'max_val': 35.51, 'sum_val': 528.94, 'row_count': 25},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-08 00:29:47.206221', 'max_ts': '2022-04-08 22:00:46.390063', 'min_val': 4.08, 'avg_val': 20.985263, 'max_val': 47.39, 'sum_val': 398.72, 'row_count': 19},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-08 00:41:46.377099', 'max_ts': '2022-04-08 23:07:46.427003', 'min_val': 0.22, 'avg_val': 5.261071, 'max_val': 10.26, 'sum_val': 147.31, 'row_count': 28},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-09 00:21:47.518132', 'max_ts': '2022-04-09 23:34:47.248113', 'min_val': 0.29, 'avg_val': 2.238214, 'max_val': 3.87, 'sum_val': 62.67, 'row_count': 28},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-09 00:16:46.098182', 'max_ts': '2022-04-09 23:55:46.825913', 'min_val': 0.36, 'avg_val': 21.998421, 'max_val': 48.63, 'sum_val': 417.97, 'row_count': 19},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-09 02:08:46.821088', 'max_ts': '2022-04-09 23:52:46.735002', 'min_val': 8.53, 'avg_val': 23.176364, 'max_val': 33.66, 'sum_val': 509.88, 'row_count': 22},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-09 00:52:47.564073', 'max_ts': '2022-04-09 23:54:47.207220', 'min_val': 1.2, 'avg_val': 30.091351, 'max_val': 48.7, 'sum_val': 1113.38, 'row_count': 37},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-09 01:02:47.517475', 'max_ts': '2022-04-09 22:50:47.511869', 'min_val': 0.42, 'avg_val': 6.344348, 'max_val': 10.64, 'sum_val': 145.92, 'row_count': 23},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-10 01:22:47.518339', 'max_ts': '2022-04-10 23:40:46.755185', 'min_val': 0.24, 'avg_val': 2.288571, 'max_val': 3.93, 'sum_val': 64.08, 'row_count': 28},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-10 01:33:46.379049', 'max_ts': '2022-04-10 23:45:46.082745', 'min_val': 0.49, 'avg_val': 23.31, 'max_val': 47.19, 'sum_val': 559.44, 'row_count': 24},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-10 01:20:46.826264', 'max_ts': '2022-04-10 22:49:46.379449', 'min_val': 2.13, 'avg_val': 21.686667, 'max_val': 34.65, 'sum_val': 585.54, 'row_count': 27},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-10 00:33:47.232539', 'max_ts': '2022-04-10 23:19:46.055374', 'min_val': 2.0, 'avg_val': 25.64, 'max_val': 45.44, 'sum_val': 615.36, 'row_count': 24},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-10 00:49:47.510319', 'max_ts': '2022-04-10 23:53:46.389384', 'min_val': 0.34, 'avg_val': 5.043913, 'max_val': 8.56, 'sum_val': 116.01, 'row_count': 23},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-11 00:18:46.752710', 'max_ts': '2022-04-11 23:33:46.733276', 'min_val': 0.14, 'avg_val': 2.000357, 'max_val': 3.9, 'sum_val': 56.01, 'row_count': 28},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-11 00:50:46.047613', 'max_ts': '2022-04-11 23:21:46.834439', 'min_val': 0.17, 'avg_val': 23.295, 'max_val': 48.44, 'sum_val': 512.49, 'row_count': 22},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-11 00:10:46.731507', 'max_ts': '2022-04-11 20:57:46.753827', 'min_val': 4.04, 'avg_val': 18.655, 'max_val': 35.38, 'sum_val': 447.72, 'row_count': 24},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-11 00:20:47.521741', 'max_ts': '2022-04-11 23:45:47.524446', 'min_val': 0.6, 'avg_val': 25.228889, 'max_val': 48.79, 'sum_val': 681.18, 'row_count': 27},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-11 00:14:46.409315', 'max_ts': '2022-04-11 23:53:47.516667', 'min_val': 0.63, 'avg_val': 5.849655, 'max_val': 10.99, 'sum_val': 169.64, 'row_count': 29},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-12 00:19:46.407815', 'max_ts': '2022-04-12 23:56:46.759892', 'min_val': 0.08, 'avg_val': 1.862, 'max_val': 3.87, 'sum_val': 55.86, 'row_count': 30},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-12 01:08:46.383316', 'max_ts': '2022-04-12 23:47:47.215069', 'min_val': 0.68, 'avg_val': 24.14, 'max_val': 48.5, 'sum_val': 627.64, 'row_count': 26},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-12 00:06:46.421489', 'max_ts': '2022-04-12 23:29:47.250430', 'min_val': 6.31, 'avg_val': 18.667297, 'max_val': 36.92, 'sum_val': 690.69, 'row_count': 37},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-12 01:38:46.062132', 'max_ts': '2022-04-12 22:38:46.048491', 'min_val': 3.12, 'avg_val': 24.828261, 'max_val': 43.49, 'sum_val': 571.05, 'row_count': 23},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-12 00:06:47.210984', 'max_ts': '2022-04-12 22:52:47.208862', 'min_val': 0.24, 'avg_val': 5.142917, 'max_val': 10.52, 'sum_val': 246.86, 'row_count': 48},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-13 00:17:46.758924', 'max_ts': '2022-04-13 22:53:47.533648', 'min_val': 0.02, 'avg_val': 1.841111, 'max_val': 3.89, 'sum_val': 49.71, 'row_count': 27},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-13 00:20:47.532696', 'max_ts': '2022-04-13 23:51:46.079040', 'min_val': 1.57, 'avg_val': 26.987391, 'max_val': 47.76, 'sum_val': 620.71, 'row_count': 23},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-13 00:47:46.418683', 'max_ts': '2022-04-13 23:59:47.536930', 'min_val': 2.03, 'avg_val': 20.425667, 'max_val': 36.02, 'sum_val': 612.77, 'row_count': 30},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-13 00:54:47.549863', 'max_ts': '2022-04-13 22:58:46.426069', 'min_val': 2.3, 'avg_val': 20.731515, 'max_val': 46.09, 'sum_val': 684.14, 'row_count': 33},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-13 00:03:46.731712', 'max_ts': '2022-04-13 23:42:46.381817', 'min_val': 0.24, 'avg_val': 5.331471, 'max_val': 10.87, 'sum_val': 181.27, 'row_count': 34},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-14 00:16:46.103756', 'max_ts': '2022-04-14 23:35:46.425955', 'min_val': 0.24, 'avg_val': 2.487308, 'max_val': 3.84, 'sum_val': 64.67, 'row_count': 26},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-14 00:08:47.210957', 'max_ts': '2022-04-14 23:04:47.565266', 'min_val': 2.24, 'avg_val': 23.622812, 'max_val': 45.33, 'sum_val': 755.93, 'row_count': 32},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-14 00:00:47.197981', 'max_ts': '2022-04-14 22:52:47.518726', 'min_val': 2.07, 'avg_val': 15.256786, 'max_val': 35.69, 'sum_val': 427.19, 'row_count': 28},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-14 00:43:46.383571', 'max_ts': '2022-04-14 23:40:47.530353', 'min_val': 0.67, 'avg_val': 20.05, 'max_val': 44.41, 'sum_val': 601.5, 'row_count': 30},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-14 00:26:46.079578', 'max_ts': '2022-04-14 23:17:46.103727', 'min_val': 0.03, 'avg_val': 4.621667, 'max_val': 9.36, 'sum_val': 110.92, 'row_count': 24},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-15 01:36:46.410228', 'max_ts': '2022-04-15 22:37:47.197696', 'min_val': 0.04, 'avg_val': 1.861481, 'max_val': 3.97, 'sum_val': 50.26, 'row_count': 27},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-15 22:09:47.198635', 'min_val': 2.94, 'avg_val': 17.53, 'max_val': 42.83, 'sum_val': 385.66, 'row_count': 22},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-15 00:56:47.220851', 'max_ts': '2022-04-15 23:03:46.793179', 'min_val': 5.64, 'avg_val': 23.799, 'max_val': 36.99, 'sum_val': 713.97, 'row_count': 30},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-15 23:19:47.546767', 'min_val': 2.57, 'avg_val': 23.805926, 'max_val': 46.38, 'sum_val': 642.76, 'row_count': 27},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-15 22:45:46.053343', 'min_val': 0.29, 'avg_val': 5.5528, 'max_val': 10.48, 'sum_val': 138.82, 'row_count': 25},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-16 00:00:47.538838', 'max_ts': '2022-04-16 18:52:46.397543', 'min_val': 0.19, 'avg_val': 2.42625, 'max_val': 3.95, 'sum_val': 38.82, 'row_count': 16},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-16 00:03:47.231798', 'max_ts': '2022-04-16 19:11:46.820956', 'min_val': 5.7, 'avg_val': 26.653571, 'max_val': 42.0, 'sum_val': 373.15, 'row_count': 14},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-16 03:48:47.506544', 'max_ts': '2022-04-16 16:24:47.211497', 'min_val': 10.03, 'avg_val': 18.021429, 'max_val': 28.38, 'sum_val': 126.15, 'row_count': 7},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-16 00:42:47.564284', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 2.06, 'avg_val': 19.847273, 'max_val': 33.52, 'sum_val': 218.32, 'row_count': 11},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-16 00:04:46.747923', 'max_ts': '2022-04-16 14:14:46.733533', 'min_val': 0.03, 'avg_val': 5.891429, 'max_val': 10.8, 'sum_val': 82.48, 'row_count': 14}]

    def test_increments_6hours(self):
        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-15 00:00:00\' AND timestamp <= \'2022-04-17 23:59:59\' GROUP BY device_name '
                +' ORDER BY min_ts, device_name  DESC;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert  result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-15 01:36:46.410228', 'max_ts': '2022-04-15 03:56:47.229134', 'min_val': 0.14, 'avg_val': 1.23, 'max_val': 3.23, 'sum_val': 7.38, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-15 05:43:47.243498', 'min_val': 3.39, 'avg_val': 12.72, 'max_val': 28.75, 'sum_val': 38.16, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-15 00:56:47.220851', 'max_ts': '2022-04-15 05:51:46.816577', 'min_val': 5.89, 'avg_val': 25.741111, 'max_val': 36.97, 'sum_val': 231.67, 'row_count': 9},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-15 02:53:46.402795', 'min_val': 9.22, 'avg_val': 24.465, 'max_val': 41.59, 'sum_val': 146.79, 'row_count': 6},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-15 05:00:46.054114', 'min_val': 3.2, 'avg_val': 6.206667, 'max_val': 8.2, 'sum_val': 18.62, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-15 06:05:46.063579', 'max_ts': '2022-04-15 11:23:47.249472', 'min_val': 1.14, 'avg_val': 2.41625, 'max_val': 3.5, 'sum_val': 19.33, 'row_count': 8},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-15 08:58:46.421659', 'max_ts': '2022-04-15 11:46:46.066620', 'min_val': 4.13, 'avg_val': 14.8, 'max_val': 27.41, 'sum_val': 74.0, 'row_count': 5},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-15 06:18:46.069512', 'max_ts': '2022-04-15 11:21:46.072482', 'min_val': 5.64, 'avg_val': 18.18125, 'max_val': 36.99, 'sum_val': 145.45, 'row_count': 8},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-15 07:15:47.519525', 'max_ts': '2022-04-15 10:25:46.813142', 'min_val': 2.57, 'avg_val': 17.85, 'max_val': 31.19, 'sum_val': 160.65, 'row_count': 9},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-15 07:59:46.047977', 'max_ts': '2022-04-15 11:01:46.101973', 'min_val': 0.29, 'avg_val': 2.676, 'max_val': 7.26, 'sum_val': 13.38, 'row_count': 5},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-15 13:00:47.199244', 'max_ts': '2022-04-15 16:55:46.400754', 'min_val': 0.04, 'avg_val': 2.256667, 'max_val': 3.97, 'sum_val': 13.54, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-15 13:33:47.525879', 'max_ts': '2022-04-15 17:11:46.058921', 'min_val': 14.54, 'avg_val': 29.636667, 'max_val': 42.83, 'sum_val': 177.82, 'row_count': 6},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-15 12:11:46.077883', 'max_ts': '2022-04-15 17:27:47.532001', 'min_val': 19.55, 'avg_val': 28.392, 'max_val': 35.29, 'sum_val': 141.96, 'row_count': 5},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-15 12:34:47.251444', 'max_ts': '2022-04-15 17:23:46.082653', 'min_val': 5.72, 'avg_val': 25.598, 'max_val': 43.64, 'sum_val': 127.99, 'row_count': 5},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-15 12:20:46.380872', 'max_ts': '2022-04-15 17:28:46.401307', 'min_val': 0.49, 'avg_val': 5.802, 'max_val': 10.48, 'sum_val': 58.02, 'row_count': 10},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-15 18:22:47.240612', 'max_ts': '2022-04-15 22:37:47.197696', 'min_val': 0.08, 'avg_val': 1.43, 'max_val': 3.73, 'sum_val': 10.01, 'row_count': 7},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-15 18:03:47.525652', 'max_ts': '2022-04-15 22:09:47.198635', 'min_val': 2.94, 'avg_val': 11.96, 'max_val': 33.62, 'sum_val': 95.68, 'row_count': 8},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-15 18:10:47.563443', 'max_ts': '2022-04-15 23:03:46.793179', 'min_val': 14.13, 'avg_val': 24.36125, 'max_val': 32.63, 'sum_val': 194.89, 'row_count': 8},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-15 19:18:46.102418', 'max_ts': '2022-04-15 23:19:47.546767', 'min_val': 5.45, 'avg_val': 29.618571, 'max_val': 46.38, 'sum_val': 207.33, 'row_count': 7},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-15 18:08:46.754689', 'max_ts': '2022-04-15 22:45:46.053343', 'min_val': 2.21, 'avg_val': 6.971429, 'max_val': 9.59, 'sum_val': 48.8, 'row_count': 7},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-16 00:00:47.538838', 'max_ts': '2022-04-16 05:59:47.249159', 'min_val': 0.19, 'avg_val': 1.782, 'max_val': 3.44, 'sum_val': 8.91, 'row_count': 5},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-16 00:03:47.231798', 'max_ts': '2022-04-16 05:47:46.063134', 'min_val': 5.89, 'avg_val': 23.988571, 'max_val': 37.74, 'sum_val': 167.92, 'row_count': 7},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-16 03:48:47.506544', 'max_ts': '2022-04-16 04:44:47.523380', 'min_val': 14.22, 'avg_val': 20.36, 'max_val': 28.38, 'sum_val': 81.44, 'row_count': 4},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-16 00:42:47.564284', 'max_ts': '2022-04-16 05:37:47.536379', 'min_val': 10.23, 'avg_val': 22.004, 'max_val': 30.81, 'sum_val': 110.02, 'row_count': 5},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-16 00:04:46.747923', 'max_ts': '2022-04-16 05:05:46.055077', 'min_val': 7.73, 'avg_val': 9.02, 'max_val': 10.31, 'sum_val': 18.04, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-16 06:36:46.369390', 'max_ts': '2022-04-16 11:00:46.389838', 'min_val': 0.74, 'avg_val': 1.953333, 'max_val': 2.92, 'sum_val': 5.86, 'row_count': 3},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-16 06:58:46.056981', 'max_ts': '2022-04-16 08:58:46.389582', 'min_val': 23.91, 'avg_val': 32.2525, 'max_val': 42.0, 'sum_val': 129.01, 'row_count': 4},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-16 09:27:46.070019', 'max_ts': '2022-04-16 09:27:46.070019', 'min_val': 22.91, 'avg_val': 22.91, 'max_val': 22.91, 'sum_val': 22.91, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-16 10:58:46.384895', 'max_ts': '2022-04-16 11:22:47.564749', 'min_val': 2.06, 'avg_val': 17.79, 'max_val': 33.52, 'sum_val': 35.58, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-16 06:24:46.424086', 'max_ts': '2022-04-16 11:49:46.413342', 'min_val': 0.03, 'avg_val': 4.943333, 'max_val': 10.8, 'sum_val': 44.49, 'row_count': 9},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-16 12:51:46.738342', 'max_ts': '2022-04-16 17:43:46.047132', 'min_val': 1.93, 'avg_val': 3.168333, 'max_val': 3.95, 'sum_val': 19.01, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-16 12:53:46.064654', 'max_ts': '2022-04-16 13:18:46.391552', 'min_val': 5.7, 'avg_val': 22.04, 'max_val': 38.38, 'sum_val': 44.08, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-16 13:57:47.220822', 'max_ts': '2022-04-16 16:24:47.211497', 'min_val': 10.03, 'avg_val': 10.9, 'max_val': 11.77, 'sum_val': 21.8, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-16 12:45:47.528428', 'max_ts': '2022-04-16 15:22:46.096679', 'min_val': 5.54, 'avg_val': 9.815, 'max_val': 14.09, 'sum_val': 19.63, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-16 12:35:46.101564', 'max_ts': '2022-04-16 14:14:46.733533', 'min_val': 4.02, 'avg_val': 6.65, 'max_val': 10.8, 'sum_val': 19.95, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-16 18:19:46.773887', 'max_ts': '2022-04-16 18:52:46.397543', 'min_val': 1.18, 'avg_val': 2.52, 'max_val': 3.86, 'sum_val': 5.04, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-16 19:11:46.820956', 'max_ts': '2022-04-16 19:11:46.820956', 'min_val': 32.14, 'avg_val': 32.14, 'max_val': 32.14, 'sum_val': 32.14, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-16 18:27:47.550771', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 26.53, 'avg_val': 26.545, 'max_val': 26.56, 'sum_val': 53.09, 'row_count': 2}]

    def test_increments_1hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), parentelement, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-15 00:00:00\' AND timestamp <= \'2022-04-15 23:59:59\' GROUP BY parentelement '
                +' ORDER BY min_ts, parentelement  DESC;"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)
        assert result == [{'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-15 00:09:46.421460', 'min_val': 7.22, 'avg_val': 7.22, 'max_val': 7.22, 'sum_val': 7.22, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-15 00:10:47.518961', 'min_val': 3.39, 'avg_val': 3.39, 'max_val': 3.39, 'sum_val': 3.39, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-15 00:42:47.521380', 'min_val': 35.58, 'avg_val': 35.93, 'max_val': 36.28, 'sum_val': 71.86, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:56:47.220851', 'max_ts': '2022-04-15 00:56:47.220851', 'min_val': 14.53, 'avg_val': 14.53, 'max_val': 14.53, 'sum_val': 14.53, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 01:36:46.410228', 'max_ts': '2022-04-15 01:36:46.410228', 'min_val': 3.23, 'avg_val': 3.23, 'max_val': 3.23, 'sum_val': 3.23, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 01:03:46.056865', 'max_ts': '2022-04-15 01:03:46.056865', 'min_val': 6.02, 'avg_val': 6.02, 'max_val': 6.02, 'sum_val': 6.02, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 01:46:47.537701', 'max_ts': '2022-04-15 01:46:47.537701', 'min_val': 41.59, 'avg_val': 41.59, 'max_val': 41.59, 'sum_val': 41.59, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 01:55:46.056274', 'max_ts': '2022-04-15 01:55:46.056274', 'min_val': 18.51, 'avg_val': 18.51, 'max_val': 18.51, 'sum_val': 18.51, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 02:09:46.053313', 'max_ts': '2022-04-15 02:09:46.053313', 'min_val': 1.42, 'avg_val': 1.42, 'max_val': 1.42, 'sum_val': 1.42, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 02:03:46.406299', 'max_ts': '2022-04-15 02:53:46.402795', 'min_val': 9.22, 'avg_val': 11.113333, 'max_val': 14.45, 'sum_val': 33.34, 'row_count': 3},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 03:54:46.104760', 'max_ts': '2022-04-15 03:54:46.104760', 'min_val': 8.2, 'avg_val': 8.2, 'max_val': 8.2, 'sum_val': 8.2, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 03:14:46.047674', 'max_ts': '2022-04-15 03:56:47.229134', 'min_val': 0.14, 'avg_val': 0.6825, 'max_val': 2.09, 'sum_val': 2.73, 'row_count': 4},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 03:28:46.743603', 'max_ts': '2022-04-15 03:44:47.232096', 'min_val': 5.89, 'avg_val': 18.165, 'max_val': 30.44, 'sum_val': 36.33, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 04:27:46.070522', 'max_ts': '2022-04-15 04:29:47.529292', 'min_val': 29.59, 'avg_val': 30.695, 'max_val': 31.8, 'sum_val': 61.39, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 05:00:46.054114', 'max_ts': '2022-04-15 05:00:46.054114', 'min_val': 3.2, 'avg_val': 3.2, 'max_val': 3.2, 'sum_val': 3.2, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 05:43:47.243498', 'max_ts': '2022-04-15 05:43:47.243498', 'min_val': 28.75, 'avg_val': 28.75, 'max_val': 28.75, 'sum_val': 28.75, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 05:22:46.392725', 'max_ts': '2022-04-15 05:51:46.816577', 'min_val': 29.5, 'avg_val': 33.636667, 'max_val': 36.97, 'sum_val': 100.91, 'row_count': 3},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 06:05:46.063579', 'max_ts': '2022-04-15 06:18:46.082114', 'min_val': 1.14, 'avg_val': 1.33, 'max_val': 1.52, 'sum_val': 2.66, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 06:18:46.069512', 'max_ts': '2022-04-15 06:48:46.746760', 'min_val': 23.9, 'avg_val': 30.445, 'max_val': 36.99, 'sum_val': 60.89, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 07:59:46.047977', 'max_ts': '2022-04-15 07:59:46.047977', 'min_val': 3.87, 'avg_val': 3.87, 'max_val': 3.87, 'sum_val': 3.87, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 07:23:47.203104', 'max_ts': '2022-04-15 07:23:47.203104', 'min_val': 1.96, 'avg_val': 1.96, 'max_val': 1.96, 'sum_val': 1.96, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 07:15:47.519525', 'max_ts': '2022-04-15 07:32:46.379020', 'min_val': 15.57, 'avg_val': 22.306667, 'max_val': 27.62, 'sum_val': 66.92, 'row_count': 3},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 08:33:46.418228', 'max_ts': '2022-04-15 08:33:46.418228', 'min_val': 0.29, 'avg_val': 0.29, 'max_val': 0.29, 'sum_val': 0.29, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 08:58:46.421659', 'max_ts': '2022-04-15 08:58:46.421659', 'min_val': 13.05, 'avg_val': 13.05, 'max_val': 13.05, 'sum_val': 13.05, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 08:55:46.369332', 'max_ts': '2022-04-15 08:57:46.811078', 'min_val': 6.27, 'avg_val': 21.4225, 'max_val': 31.19, 'sum_val': 85.69, 'row_count': 4},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 08:15:47.546474', 'max_ts': '2022-04-15 08:51:46.807225', 'min_val': 5.64, 'avg_val': 10.145, 'max_val': 14.65, 'sum_val': 20.29, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 09:04:47.234703', 'max_ts': '2022-04-15 09:38:47.527813', 'min_val': 0.56, 'avg_val': 0.98, 'max_val': 1.4, 'sum_val': 1.96, 'row_count': 2},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 09:56:47.524532', 'max_ts': '2022-04-15 09:56:47.524532', 'min_val': 3.5, 'avg_val': 3.5, 'max_val': 3.5, 'sum_val': 3.5, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 09:48:46.825626', 'max_ts': '2022-04-15 09:56:47.519583', 'min_val': 4.13, 'avg_val': 13.52, 'max_val': 22.91, 'sum_val': 27.04, 'row_count': 2},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 09:56:47.226475', 'max_ts': '2022-04-15 09:56:47.226475', 'min_val': 5.47, 'avg_val': 5.47, 'max_val': 5.47, 'sum_val': 5.47, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 10:16:47.193110', 'max_ts': '2022-04-15 10:48:46.090076', 'min_val': 1.81, 'avg_val': 2.593333, 'max_val': 3.35, 'sum_val': 7.78, 'row_count': 3},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 10:25:46.813142', 'max_ts': '2022-04-15 10:25:46.813142', 'min_val': 2.57, 'avg_val': 2.57, 'max_val': 2.57, 'sum_val': 2.57, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 10:02:47.553436', 'max_ts': '2022-04-15 10:20:47.565122', 'min_val': 7.52, 'avg_val': 20.32, 'max_val': 33.12, 'sum_val': 40.64, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 11:01:46.101973', 'max_ts': '2022-04-15 11:01:46.101973', 'min_val': 7.26, 'avg_val': 7.26, 'max_val': 7.26, 'sum_val': 7.26, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 11:23:47.249472', 'max_ts': '2022-04-15 11:23:47.249472', 'min_val': 3.43, 'avg_val': 3.43, 'max_val': 3.43, 'sum_val': 3.43, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 11:34:46.395429', 'max_ts': '2022-04-15 11:46:46.066620', 'min_val': 6.5, 'avg_val': 16.955, 'max_val': 27.41, 'sum_val': 33.91, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 11:14:46.094001', 'max_ts': '2022-04-15 11:21:46.072482', 'min_val': 6.16, 'avg_val': 11.815, 'max_val': 17.47, 'sum_val': 23.63, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 12:20:46.380872', 'max_ts': '2022-04-15 12:49:47.215726', 'min_val': 2.08, 'avg_val': 6.28, 'max_val': 10.48, 'sum_val': 12.56, 'row_count': 2},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 12:34:47.251444', 'max_ts': '2022-04-15 12:54:47.227353', 'min_val': 5.72, 'avg_val': 24.68, 'max_val': 43.64, 'sum_val': 49.36, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 12:11:46.077883', 'max_ts': '2022-04-15 12:11:46.077883', 'min_val': 22.26, 'avg_val': 22.26, 'max_val': 22.26, 'sum_val': 22.26, 'row_count': 1},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 13:15:46.741026', 'max_ts': '2022-04-15 13:54:47.555364', 'min_val': 4.25, 'avg_val': 7.226667, 'max_val': 8.74, 'sum_val': 21.68, 'row_count': 3},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 13:00:47.199244', 'max_ts': '2022-04-15 13:15:46.369275', 'min_val': 0.04, 'avg_val': 0.605, 'max_val': 1.17, 'sum_val': 1.21, 'row_count': 2},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 13:33:47.525879', 'max_ts': '2022-04-15 13:33:47.525879', 'min_val': 20.46, 'avg_val': 20.46, 'max_val': 20.46, 'sum_val': 20.46, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 13:21:46.092642', 'max_ts': '2022-04-15 13:21:46.092642', 'min_val': 19.55, 'avg_val': 19.55, 'max_val': 19.55, 'sum_val': 19.55, 'row_count': 1},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 14:07:46.391234', 'max_ts': '2022-04-15 14:07:46.391234', 'min_val': 0.49, 'avg_val': 0.49, 'max_val': 0.49, 'sum_val': 0.49, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 14:52:46.836527', 'max_ts': '2022-04-15 14:52:46.836527', 'min_val': 2.96, 'avg_val': 2.96, 'max_val': 2.96, 'sum_val': 2.96, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 14:41:47.534223', 'max_ts': '2022-04-15 14:41:47.534223', 'min_val': 34.17, 'avg_val': 34.17, 'max_val': 34.17, 'sum_val': 34.17, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 14:35:47.516258', 'max_ts': '2022-04-15 14:35:47.516258', 'min_val': 14.15, 'avg_val': 14.15, 'max_val': 14.15, 'sum_val': 14.15, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 14:12:46.398511', 'max_ts': '2022-04-15 14:12:46.398511', 'min_val': 32.8, 'avg_val': 32.8, 'max_val': 32.8, 'sum_val': 32.8, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 15:01:47.237180', 'max_ts': '2022-04-15 15:54:46.394967', 'min_val': 1.55, 'avg_val': 2.76, 'max_val': 3.97, 'sum_val': 5.52, 'row_count': 2},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 15:38:47.213196', 'max_ts': '2022-04-15 15:38:47.213196', 'min_val': 35.59, 'avg_val': 35.59, 'max_val': 35.59, 'sum_val': 35.59, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 15:18:46.069755', 'max_ts': '2022-04-15 15:18:46.069755', 'min_val': 32.06, 'avg_val': 32.06, 'max_val': 32.06, 'sum_val': 32.06, 'row_count': 1},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 16:16:46.378390', 'max_ts': '2022-04-15 16:55:46.081701', 'min_val': 3.19, 'avg_val': 6.635, 'max_val': 10.08, 'sum_val': 13.27, 'row_count': 2},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 16:55:46.400754', 'max_ts': '2022-04-15 16:55:46.400754', 'min_val': 3.85, 'avg_val': 3.85, 'max_val': 3.85, 'sum_val': 3.85, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 16:27:47.220645', 'max_ts': '2022-04-15 16:27:47.537203', 'min_val': 14.54, 'avg_val': 22.385, 'max_val': 30.23, 'sum_val': 44.77, 'row_count': 2},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 16:06:46.371891', 'max_ts': '2022-04-15 16:06:46.371891', 'min_val': 21.65, 'avg_val': 21.65, 'max_val': 21.65, 'sum_val': 21.65, 'row_count': 1},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 17:13:47.562601', 'max_ts': '2022-04-15 17:28:46.401307', 'min_val': 2.34, 'avg_val': 5.01, 'max_val': 7.68, 'sum_val': 10.02, 'row_count': 2},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 17:11:46.058921', 'max_ts': '2022-04-15 17:11:46.058921', 'min_val': 42.83, 'avg_val': 42.83, 'max_val': 42.83, 'sum_val': 42.83, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 17:23:46.082653', 'max_ts': '2022-04-15 17:23:46.082653', 'min_val': 42.83, 'avg_val': 42.83, 'max_val': 42.83, 'sum_val': 42.83, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 17:27:47.532001', 'max_ts': '2022-04-15 17:27:47.532001', 'min_val': 35.29, 'avg_val': 35.29, 'max_val': 35.29, 'sum_val': 35.29, 'row_count': 1},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 18:08:46.754689', 'max_ts': '2022-04-15 18:08:46.754689', 'min_val': 8.75, 'avg_val': 8.75, 'max_val': 8.75, 'sum_val': 8.75, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 18:22:47.240612', 'max_ts': '2022-04-15 18:22:47.240612', 'min_val': 0.21, 'avg_val': 0.21, 'max_val': 0.21, 'sum_val': 0.21, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 18:03:47.525652', 'max_ts': '2022-04-15 18:42:46.384195', 'min_val': 2.94, 'avg_val': 8.458, 'max_val': 15.2, 'sum_val': 42.29, 'row_count': 5},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 18:10:47.563443', 'max_ts': '2022-04-15 18:57:47.201284', 'min_val': 22.68, 'avg_val': 27.043333, 'max_val': 30.34, 'sum_val': 81.13, 'row_count': 3},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 19:05:46.756429', 'max_ts': '2022-04-15 19:38:46.752264', 'min_val': 2.21, 'avg_val': 5.9, 'max_val': 8.47, 'sum_val': 23.6, 'row_count': 4},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 19:12:46.076414', 'max_ts': '2022-04-15 19:57:46.075724', 'min_val': 0.97, 'avg_val': 1.4975, 'max_val': 2.45, 'sum_val': 5.99, 'row_count': 4},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 19:50:47.200997', 'max_ts': '2022-04-15 19:54:47.539171', 'min_val': 6.24, 'avg_val': 9.885, 'max_val': 13.53, 'sum_val': 19.77, 'row_count': 2},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 19:18:46.102418', 'max_ts': '2022-04-15 19:51:47.512902', 'min_val': 6.51, 'avg_val': 31.956667, 'max_val': 46.38, 'sum_val': 95.87, 'row_count': 3},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 19:16:46.820794', 'max_ts': '2022-04-15 19:16:46.820794', 'min_val': 32.63, 'avg_val': 32.63, 'max_val': 32.63, 'sum_val': 32.63, 'row_count': 1},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 20:09:46.808998', 'max_ts': '2022-04-15 20:09:46.808998', 'min_val': 0.08, 'avg_val': 0.08, 'max_val': 0.08, 'sum_val': 0.08, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 20:06:47.518608', 'max_ts': '2022-04-15 20:08:46.102242', 'min_val': 5.45, 'avg_val': 23.865, 'max_val': 42.28, 'sum_val': 47.73, 'row_count': 2},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 21:05:46.091270', 'max_ts': '2022-04-15 21:12:46.099052', 'min_val': 14.85, 'avg_val': 23.59, 'max_val': 32.33, 'sum_val': 47.18, 'row_count': 2},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 22:18:47.208777', 'max_ts': '2022-04-15 22:45:46.053343', 'min_val': 6.86, 'avg_val': 8.225, 'max_val': 9.59, 'sum_val': 16.45, 'row_count': 2},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 22:37:47.197696', 'max_ts': '2022-04-15 22:37:47.197696', 'min_val': 3.73, 'avg_val': 3.73, 'max_val': 3.73, 'sum_val': 3.73, 'row_count': 1},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 22:09:47.198635', 'max_ts': '2022-04-15 22:09:47.198635', 'min_val': 33.62, 'avg_val': 33.62, 'max_val': 33.62, 'sum_val': 33.62, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 22:00:46.739833', 'max_ts': '2022-04-15 22:00:46.739833', 'min_val': 37.57, 'avg_val': 37.57, 'max_val': 37.57, 'sum_val': 37.57, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 22:01:47.518903', 'max_ts': '2022-04-15 22:01:47.518903', 'min_val': 19.82, 'avg_val': 19.82, 'max_val': 19.82, 'sum_val': 19.82, 'row_count': 1},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 23:19:47.546767', 'max_ts': '2022-04-15 23:19:47.546767', 'min_val': 26.16, 'avg_val': 26.16, 'max_val': 26.16, 'sum_val': 26.16, 'row_count': 1},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 23:03:46.793179', 'max_ts': '2022-04-15 23:03:46.793179', 'min_val': 14.13, 'avg_val': 14.13, 'max_val': 14.13, 'sum_val': 14.13, 'row_count': 1}]

    def test_increments_1minute(self):
        query = (self.base_query + ' "SELECT increments(minute, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-04-15 00:00:00\' AND timestamp <= \'2022-04-15 00:59:59.999999\'"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-15 00:01:46.743220', 'min_val': 36.28, 'avg_val': 36.28, 'max_val': 36.28, 'sum_val': 36.28, 'row_count': 1},
                          {'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-15 00:09:46.421460', 'min_val': 7.22, 'avg_val': 7.22, 'max_val': 7.22, 'sum_val': 7.22, 'row_count': 1},
                          {'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-15 00:10:47.518961', 'min_val': 3.39, 'avg_val': 3.39, 'max_val': 3.39, 'sum_val': 3.39, 'row_count': 1},
                          {'min_ts': '2022-04-15 00:42:47.521380', 'max_ts': '2022-04-15 00:42:47.521380', 'min_val': 35.58, 'avg_val': 35.58, 'max_val': 35.58, 'sum_val': 35.58, 'row_count': 1},
                          {'min_ts': '2022-04-15 00:56:47.220851', 'max_ts': '2022-04-15 00:56:47.220851', 'min_val': 14.53, 'avg_val': 14.53, 'max_val': 14.53, 'sum_val': 14.53, 'row_count': 1}]

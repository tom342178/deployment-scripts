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

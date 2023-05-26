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
        cls.base_query = f"sql test format=json and stat=false and include=(percentagecpu_sensor) and extend=(@table_name as table)"

    def test_increments_1month(self):
        query = (self.base_query + ' "SELECT increments(month, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\'"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.0, 'avg_val': 50.052119, 'max_val': 99.94, 'sum_val': 104658.98, 'row_count': 2091},
                          {'table': 'ping_sensor', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.896316, 'max_val': 49.0, 'sum_val': 31888.01, 'row_count': 2006},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-01 00:03:52.726544', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.1, 'avg_val': 50.646099, 'max_val': 99.94, 'sum_val': 217221.12, 'row_count': 4289},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.0, 'avg_val': 14.877294, 'max_val': 48.98, 'sum_val': 62945.83, 'row_count': 4231},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 0.0, 'avg_val': 50.159005, 'max_val': 99.99, 'sum_val': 110399.97, 'row_count': 2201},
                          {'table': 'ping_sensor', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.01, 'avg_val': 15.118887, 'max_val': 49.0, 'sum_val': 32052.04, 'row_count': 2120}]

    def test_increments_30day(self):
        query = (self.base_query + ' "SELECT increments(day, 30, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\'"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.0, 'avg_val': 50.052119, 'max_val': 99.94, 'sum_val': 104658.98, 'row_count': 2091},
                          {'table': 'ping_sensor', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.896316, 'max_val': 49.0, 'sum_val': 31888.01, 'row_count': 2006},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-01 00:03:52.726544', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.1, 'avg_val': 50.594886, 'max_val': 99.94, 'sum_val': 203391.44, 'row_count': 4020},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.0, 'avg_val': 14.893007, 'max_val': 48.98, 'sum_val': 59095.45, 'row_count': 3968},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.29, 'avg_val': 51.41145, 'max_val': 99.5, 'sum_val': 13829.68, 'row_count': 269},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.640228, 'max_val': 48.87, 'sum_val': 3850.38, 'row_count': 263},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 0.0, 'avg_val': 50.159005, 'max_val': 99.99, 'sum_val': 110399.97, 'row_count': 2201},
                          {'table': 'ping_sensor', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.01, 'avg_val': 15.118887, 'max_val': 49.0, 'sum_val': 32052.04, 'row_count': 2120}]

    def test_increments_15day(self):
        query = (self.base_query + ' "SELECT increments(day, 15, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-05-01 00:00:00\' AND timestamp >= \'2022-02-01 00:00:00\' '
                +'ORDER BY min_ts ASC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-14 23:55:51.296406', 'min_val': 0.83, 'avg_val': 48.763205, 'max_val': 99.55, 'sum_val': 3803.53, 'row_count': 78},
                          {'table': 'ping_sensor', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-14 23:35:47.507093', 'min_val': 0.5, 'avg_val': 18.513462, 'max_val': 48.2, 'sum_val': 1444.05, 'row_count': 78},
                          {'table': 'ping_sensor', 'min_ts': '2022-02-15 00:01:46.048094', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.790436, 'max_val': 49.0, 'sum_val': 30443.96, 'row_count': 1928},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-02-15 00:05:52.386039', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.0, 'avg_val': 50.102062, 'max_val': 99.94, 'sum_val': 100855.45, 'row_count': 2013},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-14 23:43:46.381074', 'min_val': 0.0, 'avg_val': 15.156264, 'max_val': 48.98, 'sum_val': 29251.59, 'row_count': 1930},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-01 00:03:52.726544', 'max_ts': '2022-03-14 23:46:52.004831', 'min_val': 0.1, 'avg_val': 50.102958, 'max_val': 99.87, 'sum_val': 97550.46, 'row_count': 1947},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.0, 'avg_val': 14.6437, 'max_val': 48.96, 'sum_val': 29843.86, 'row_count': 2038},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.15, 'avg_val': 51.056913, 'max_val': 99.94, 'sum_val': 105840.98, 'row_count': 2073},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.29, 'avg_val': 51.41145, 'max_val': 99.5, 'sum_val': 13829.68, 'row_count': 269},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.640228, 'max_val': 48.87, 'sum_val': 3850.38, 'row_count': 263},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-14 23:45:51.249043', 'min_val': 0.0, 'avg_val': 50.199905, 'max_val': 99.99, 'sum_val': 100650.81, 'row_count': 2005},
                          {'table': 'ping_sensor', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-14 23:40:47.530353', 'min_val': 0.01, 'avg_val': 15.195459, 'max_val': 49.0, 'sum_val': 29281.65, 'row_count': 1927},
                          {'table': 'ping_sensor', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.03, 'avg_val': 14.354352, 'max_val': 46.38, 'sum_val': 2770.39, 'row_count': 193},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-04-15 00:22:52.417430', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 0.23, 'avg_val': 49.740612, 'max_val': 99.83, 'sum_val': 9749.16, 'row_count': 196}]

    def test_increments_7day(self):
        query = (self.base_query + ' "SELECT increments(day, 7, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-01 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-03-28 00:08:51.976194', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.24, 'avg_val': 50.04376, 'max_val': 99.5, 'sum_val': 26222.93, 'row_count': 524},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.606992, 'max_val': 48.87, 'sum_val': 7332.71, 'row_count': 502},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-21 00:06:51.278211', 'max_ts': '2022-03-27 23:51:51.297168', 'min_val': 0.31, 'avg_val': 52.599949, 'max_val': 99.94, 'sum_val': 51442.75, 'row_count': 978},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.01, 'avg_val': 14.447417, 'max_val': 48.84, 'sum_val': 13985.1, 'row_count': 968},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-14 00:14:46.735774', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 14.854756, 'max_val': 48.96, 'sum_val': 14305.13, 'row_count': 963},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-14 00:13:51.291886', 'max_ts': '2022-03-20 23:44:51.569172', 'min_val': 0.15, 'avg_val': 49.495976, 'max_val': 99.9, 'sum_val': 48951.52, 'row_count': 989},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-07 00:19:46.056837', 'max_ts': '2022-03-13 23:57:47.233039', 'min_val': 0.01, 'avg_val': 14.727345, 'max_val': 48.97, 'sum_val': 13755.34, 'row_count': 934},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-07 00:01:51.971909', 'max_ts': '2022-03-13 23:55:51.296840', 'min_val': 0.12, 'avg_val': 50.126614, 'max_val': 99.87, 'sum_val': 47971.17, 'row_count': 957},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-01 00:03:52.726544', 'max_ts': '2022-03-06 23:59:51.992156', 'min_val': 0.1, 'avg_val': 50.692925, 'max_val': 99.74, 'sum_val': 42632.75, 'row_count': 841},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-06 23:40:47.544449', 'min_val': 0.0, 'avg_val': 15.703183, 'max_val': 48.98, 'sum_val': 13567.55, 'row_count': 864}]

    def test_increments_1day(self):
        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        desc_result == [{'table': 'percentagecpu_sensor', 'min_ts': '2022-03-31 00:08:51.599812', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 1.49, 'avg_val': 54.20625, 'max_val': 99.41, 'sum_val': 6071.1, 'row_count': 112},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.06, 'avg_val': 15.841374, 'max_val': 48.87, 'sum_val': 2075.22, 'row_count': 131},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-30 23:37:46.062928', 'min_val': 0.02, 'avg_val': 13.448182, 'max_val': 46.87, 'sum_val': 1775.16, 'row_count': 132},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-30 23:59:51.301063', 'min_val': 0.29, 'avg_val': 49.417707, 'max_val': 99.5, 'sum_val': 7758.58, 'row_count': 157},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-29 00:19:52.741501', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.24, 'avg_val': 49.5396, 'max_val': 98.67, 'sum_val': 6192.45, 'row_count': 125},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.15, 'avg_val': 14.937521, 'max_val': 47.8, 'sum_val': 1747.69, 'row_count': 117},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-28 00:08:51.976194', 'max_ts': '2022-03-28 23:51:52.015145', 'min_val': 0.74, 'avg_val': 47.698462, 'max_val': 99.45, 'sum_val': 6200.8, 'row_count': 130},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 14.218361, 'max_val': 45.29, 'sum_val': 1734.64, 'row_count': 122},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-27 00:06:47.542971', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 14.212721, 'max_val': 48.84, 'sum_val': 2089.27, 'row_count': 147},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-27 00:03:51.269763', 'max_ts': '2022-03-27 23:51:51.297168', 'min_val': 0.63, 'avg_val': 53.354048, 'max_val': 99.77, 'sum_val': 6722.61, 'row_count': 126},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-26 00:17:51.248953', 'max_ts': '2022-03-26 23:49:51.958118', 'min_val': 0.31, 'avg_val': 50.051181, 'max_val': 97.64, 'sum_val': 7207.37, 'row_count': 144},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 14.736443, 'max_val': 48.06, 'sum_val': 2195.73, 'row_count': 149},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-25 00:01:51.301895', 'max_ts': '2022-03-25 23:44:52.752827', 'min_val': 0.75, 'avg_val': 52.510872, 'max_val': 98.19, 'sum_val': 7824.12, 'row_count': 149},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 15.347482, 'max_val': 47.1, 'sum_val': 2133.3, 'row_count': 139},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-24 00:36:46.074681', 'max_ts': '2022-03-24 23:26:47.195182', 'min_val': 0.01, 'avg_val': 13.136797, 'max_val': 48.29, 'sum_val': 1681.51, 'row_count': 128},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-24 00:23:52.386471', 'max_ts': '2022-03-24 23:58:51.277280', 'min_val': 1.66, 'avg_val': 54.588372, 'max_val': 99.94, 'sum_val': 7041.9, 'row_count': 129},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-23 00:13:52.745707', 'max_ts': '2022-03-23 23:54:52.391815', 'min_val': 3.51, 'avg_val': 52.900728, 'max_val': 99.64, 'sum_val': 7988.01, 'row_count': 151},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 13.265349, 'max_val': 48.45, 'sum_val': 1711.23, 'row_count': 129},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-22 00:09:46.389923', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 14.310621, 'max_val': 43.64, 'sum_val': 2075.04, 'row_count': 145},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-22 00:06:51.619546', 'max_ts': '2022-03-22 23:46:51.957737', 'min_val': 1.24, 'avg_val': 50.610274, 'max_val': 99.76, 'sum_val': 7389.1, 'row_count': 146},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-21 00:06:51.278211', 'max_ts': '2022-03-21 23:52:51.587190', 'min_val': 0.55, 'avg_val': 54.658947, 'max_val': 99.91, 'sum_val': 7269.64, 'row_count': 133},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:33:46.385868', 'min_val': 0.04, 'avg_val': 16.023053, 'max_val': 47.44, 'sum_val': 2099.02, 'row_count': 131},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-20 00:07:51.595366', 'max_ts': '2022-03-20 23:44:51.569172', 'min_val': 0.25, 'avg_val': 49.085592, 'max_val': 99.77, 'sum_val': 7461.01, 'row_count': 152},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 13.752963, 'max_val': 48.96, 'sum_val': 1856.65, 'row_count': 135},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-19 00:08:46.092527', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 15.034155, 'max_val': 48.05, 'sum_val': 2134.85, 'row_count': 142},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-19 00:00:52.400235', 'max_ts': '2022-03-19 23:42:52.733133', 'min_val': 1.1, 'avg_val': 49.757852, 'max_val': 96.41, 'sum_val': 6717.31, 'row_count': 135},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-18 00:20:51.290505', 'max_ts': '2022-03-18 23:52:51.984613', 'min_val': 0.15, 'avg_val': 50.219934, 'max_val': 99.9, 'sum_val': 7583.21, 'row_count': 151},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 13.823231, 'max_val': 48.87, 'sum_val': 1797.02, 'row_count': 130},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-17 00:08:47.216280', 'max_ts': '2022-03-17 23:53:47.507880', 'min_val': 0.21, 'avg_val': 16.661135, 'max_val': 48.87, 'sum_val': 2349.22, 'row_count': 141},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-17 00:01:51.600314', 'max_ts': '2022-03-17 23:58:52.424868', 'min_val': 1.09, 'avg_val': 48.634632, 'max_val': 98.16, 'sum_val': 6614.31, 'row_count': 136},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-16 00:09:46.068468', 'max_ts': '2022-03-16 23:56:47.244853', 'min_val': 0.03, 'avg_val': 15.440861, 'max_val': 48.07, 'sum_val': 2331.57, 'row_count': 151},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-16 00:07:52.385601', 'max_ts': '2022-03-16 23:59:51.964092', 'min_val': 0.5, 'avg_val': 49.611159, 'max_val': 97.37, 'sum_val': 6846.34, 'row_count': 138},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 0.59, 'avg_val': 52.990625, 'max_val': 99.51, 'sum_val': 6782.8, 'row_count': 128},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 0.0, 'avg_val': 14.447879, 'max_val': 47.44, 'sum_val': 1907.12, 'row_count': 132}]

        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert asc_result == [{'table': 'ping_sensor', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 0.0, 'avg_val': 14.447879, 'max_val': 47.44, 'sum_val': 1907.12, 'row_count': 132},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 0.59, 'avg_val': 52.990625, 'max_val': 99.51, 'sum_val': 6782.8, 'row_count': 128},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-16 00:07:52.385601', 'max_ts': '2022-03-16 23:59:51.964092', 'min_val': 0.5, 'avg_val': 49.611159, 'max_val': 97.37, 'sum_val': 6846.34, 'row_count': 138},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-16 00:09:46.068468', 'max_ts': '2022-03-16 23:56:47.244853', 'min_val': 0.03, 'avg_val': 15.440861, 'max_val': 48.07, 'sum_val': 2331.57, 'row_count': 151},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-17 00:01:51.600314', 'max_ts': '2022-03-17 23:58:52.424868', 'min_val': 1.09, 'avg_val': 48.634632, 'max_val': 98.16, 'sum_val': 6614.31, 'row_count': 136},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-17 00:08:47.216280', 'max_ts': '2022-03-17 23:53:47.507880', 'min_val': 0.21, 'avg_val': 16.661135, 'max_val': 48.87, 'sum_val': 2349.22, 'row_count': 141},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 13.823231, 'max_val': 48.87, 'sum_val': 1797.02, 'row_count': 130},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-18 00:20:51.290505', 'max_ts': '2022-03-18 23:52:51.984613', 'min_val': 0.15, 'avg_val': 50.219934, 'max_val': 99.9, 'sum_val': 7583.21, 'row_count': 151},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-19 00:00:52.400235', 'max_ts': '2022-03-19 23:42:52.733133', 'min_val': 1.1, 'avg_val': 49.757852, 'max_val': 96.41, 'sum_val': 6717.31, 'row_count': 135},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-19 00:08:46.092527', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 15.034155, 'max_val': 48.05, 'sum_val': 2134.85, 'row_count': 142},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 13.752963, 'max_val': 48.96, 'sum_val': 1856.65, 'row_count': 135},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-20 00:07:51.595366', 'max_ts': '2022-03-20 23:44:51.569172', 'min_val': 0.25, 'avg_val': 49.085592, 'max_val': 99.77, 'sum_val': 7461.01, 'row_count': 152},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:33:46.385868', 'min_val': 0.04, 'avg_val': 16.023053, 'max_val': 47.44, 'sum_val': 2099.02, 'row_count': 131},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-21 00:06:51.278211', 'max_ts': '2022-03-21 23:52:51.587190', 'min_val': 0.55, 'avg_val': 54.658947, 'max_val': 99.91, 'sum_val': 7269.64, 'row_count': 133},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-22 00:06:51.619546', 'max_ts': '2022-03-22 23:46:51.957737', 'min_val': 1.24, 'avg_val': 50.610274, 'max_val': 99.76, 'sum_val': 7389.1, 'row_count': 146},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-22 00:09:46.389923', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 14.310621, 'max_val': 43.64, 'sum_val': 2075.04, 'row_count': 145},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 13.265349, 'max_val': 48.45, 'sum_val': 1711.23, 'row_count': 129},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-23 00:13:52.745707', 'max_ts': '2022-03-23 23:54:52.391815', 'min_val': 3.51, 'avg_val': 52.900728, 'max_val': 99.64, 'sum_val': 7988.01, 'row_count': 151},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-24 00:23:52.386471', 'max_ts': '2022-03-24 23:58:51.277280', 'min_val': 1.66, 'avg_val': 54.588372, 'max_val': 99.94, 'sum_val': 7041.9, 'row_count': 129},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-24 00:36:46.074681', 'max_ts': '2022-03-24 23:26:47.195182', 'min_val': 0.01, 'avg_val': 13.136797, 'max_val': 48.29, 'sum_val': 1681.51, 'row_count': 128},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 15.347482, 'max_val': 47.1, 'sum_val': 2133.3, 'row_count': 139},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-25 00:01:51.301895', 'max_ts': '2022-03-25 23:44:52.752827', 'min_val': 0.75, 'avg_val': 52.510872, 'max_val': 98.19, 'sum_val': 7824.12, 'row_count': 149},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 14.736443, 'max_val': 48.06, 'sum_val': 2195.73, 'row_count': 149},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-26 00:17:51.248953', 'max_ts': '2022-03-26 23:49:51.958118', 'min_val': 0.31, 'avg_val': 50.051181, 'max_val': 97.64, 'sum_val': 7207.37, 'row_count': 144},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-27 00:03:51.269763', 'max_ts': '2022-03-27 23:51:51.297168', 'min_val': 0.63, 'avg_val': 53.354048, 'max_val': 99.77, 'sum_val': 6722.61, 'row_count': 126},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-27 00:06:47.542971', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 14.212721, 'max_val': 48.84, 'sum_val': 2089.27, 'row_count': 147},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 14.218361, 'max_val': 45.29, 'sum_val': 1734.64, 'row_count': 122},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-28 00:08:51.976194', 'max_ts': '2022-03-28 23:51:52.015145', 'min_val': 0.74, 'avg_val': 47.698462, 'max_val': 99.45, 'sum_val': 6200.8, 'row_count': 130},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.15, 'avg_val': 14.937521, 'max_val': 47.8, 'sum_val': 1747.69, 'row_count': 117},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-29 00:19:52.741501', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.24, 'avg_val': 49.5396, 'max_val': 98.67, 'sum_val': 6192.45, 'row_count': 125},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-30 23:59:51.301063', 'min_val': 0.29, 'avg_val': 49.417707, 'max_val': 99.5, 'sum_val': 7758.58, 'row_count': 157},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-30 23:37:46.062928', 'min_val': 0.02, 'avg_val': 13.448182, 'max_val': 46.87, 'sum_val': 1775.16, 'row_count': 132},
                          {'table': 'ping_sensor', 'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.06, 'avg_val': 15.841374, 'max_val': 48.87, 'sum_val': 2075.22, 'row_count': 131},
                          {'table': 'percentagecpu_sensor', 'min_ts': '2022-03-31 00:08:51.599812', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 1.49, 'avg_val': 54.20625, 'max_val': 99.41, 'sum_val': 6071.1, 'row_count': 112}]

        assert asc_result != desc_result

    def test_increments_12hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 45.877143, 'max_val': 91.26, 'sum_val': 642.28, 'row_count': 14},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 5.230588, 'max_val': 10.93, 'sum_val': 88.92, 'row_count': 17},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 13:15:51.298228', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 3.14, 'avg_val': 53.073, 'max_val': 97.33, 'sum_val': 1061.46, 'row_count': 20},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.1, 'avg_val': 3.92, 'max_val': 7.88, 'sum_val': 58.8, 'row_count': 15},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 21.76, 'avg_val': 51.741538, 'max_val': 97.07, 'sum_val': 672.64, 'row_count': 13},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 3.79, 'avg_val': 30.86375, 'max_val': 46.62, 'sum_val': 246.91, 'row_count': 8},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 13:14:51.301151', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 48.12, 'max_val': 97.21, 'sum_val': 384.96, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 27.790625, 'max_val': 47.44, 'sum_val': 444.65, 'row_count': 16},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 0.59, 'avg_val': 44.300714, 'max_val': 99.51, 'sum_val': 620.21, 'row_count': 14},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.267273, 'max_val': 35.91, 'sum_val': 233.94, 'row_count': 11},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 13:40:52.394269', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 24.78, 'avg_val': 65.883333, 'max_val': 99.06, 'sum_val': 988.25, 'row_count': 15},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 19.068, 'max_val': 35.06, 'sum_val': 190.68, 'row_count': 10},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 1.55, 'avg_val': 51.472308, 'max_val': 88.75, 'sum_val': 669.14, 'row_count': 13},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 18.034, 'max_val': 43.83, 'sum_val': 270.51, 'row_count': 15},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 22:33:51.964121', 'min_val': 9.09, 'avg_val': 54.314444, 'max_val': 92.11, 'sum_val': 488.83, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 20.79125, 'max_val': 45.9, 'sum_val': 332.66, 'row_count': 16},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 3.34, 'avg_val': 55.073636, 'max_val': 93.39, 'sum_val': 605.81, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 0.52, 'avg_val': 1.457, 'max_val': 2.32, 'sum_val': 14.57, 'row_count': 10},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 2.17, 'avg_val': 59.02, 'max_val': 97.55, 'sum_val': 649.22, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.21, 'avg_val': 1.82, 'max_val': 3.01, 'sum_val': 25.48, 'row_count': 14}]

        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 3.34, 'avg_val': 55.073636, 'max_val': 93.39, 'sum_val': 605.81, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 0.52, 'avg_val': 1.457, 'max_val': 2.32, 'sum_val': 14.57, 'row_count': 10},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 2.17, 'avg_val': 59.02, 'max_val': 97.55, 'sum_val': 649.22, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.21, 'avg_val': 1.82, 'max_val': 3.01, 'sum_val': 25.48, 'row_count': 14},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 1.55, 'avg_val': 51.472308, 'max_val': 88.75, 'sum_val': 669.14, 'row_count': 13},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 18.034, 'max_val': 43.83, 'sum_val': 270.51, 'row_count': 15},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 22:33:51.964121', 'min_val': 9.09, 'avg_val': 54.314444, 'max_val': 92.11, 'sum_val': 488.83, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 20.79125, 'max_val': 45.9, 'sum_val': 332.66, 'row_count': 16},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 0.59, 'avg_val': 44.300714, 'max_val': 99.51, 'sum_val': 620.21, 'row_count': 14},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.267273, 'max_val': 35.91, 'sum_val': 233.94, 'row_count': 11},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 13:40:52.394269', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 24.78, 'avg_val': 65.883333, 'max_val': 99.06, 'sum_val': 988.25, 'row_count': 15},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 19.068, 'max_val': 35.06, 'sum_val': 190.68, 'row_count': 10},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 21.76, 'avg_val': 51.741538, 'max_val': 97.07, 'sum_val': 672.64, 'row_count': 13},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 3.79, 'avg_val': 30.86375, 'max_val': 46.62, 'sum_val': 246.91, 'row_count': 8},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 13:14:51.301151', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 48.12, 'max_val': 97.21, 'sum_val': 384.96, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 27.790625, 'max_val': 47.44, 'sum_val': 444.65, 'row_count': 16},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 45.877143, 'max_val': 91.26, 'sum_val': 642.28, 'row_count': 14},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 5.230588, 'max_val': 10.93, 'sum_val': 88.92, 'row_count': 17},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 13:15:51.298228', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 3.14, 'avg_val': 53.073, 'max_val': 97.33, 'sum_val': 1061.46, 'row_count': 20},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.1, 'avg_val': 3.92, 'max_val': 7.88, 'sum_val': 58.8, 'row_count': 15}]

        assert asc_result != desc_result

    def test_increments_6hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:38:47.550949', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.33, 'avg_val': 1.867143, 'max_val': 3.01, 'sum_val': 13.07, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:28:52.706334', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 29.35, 'avg_val': 73.844, 'max_val': 97.55, 'sum_val': 369.22, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 1.772857, 'max_val': 2.88, 'sum_val': 12.41, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 15:20:51.252355', 'min_val': 2.17, 'avg_val': 46.666667, 'max_val': 83.23, 'sum_val': 280.0, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 3.34, 'avg_val': 37.635, 'max_val': 75.29, 'sum_val': 150.54, 'row_count': 4},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.4, 'avg_val': 1.764, 'max_val': 2.32, 'sum_val': 8.82, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 1.15, 'max_val': 1.96, 'sum_val': 5.75, 'row_count': 5},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 15.64, 'avg_val': 65.038571, 'max_val': 93.39, 'sum_val': 455.27, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 22:16:51.251066', 'max_ts': '2022-03-15 22:33:51.964121', 'min_val': 77.11, 'avg_val': 80.705, 'max_val': 84.3, 'sum_val': 161.41, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 21.28625, 'max_val': 37.14, 'sum_val': 170.29, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 20.29625, 'max_val': 45.9, 'sum_val': 162.37, 'row_count': 8},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 16:58:51.988529', 'min_val': 9.09, 'avg_val': 46.774286, 'max_val': 92.11, 'sum_val': 327.42, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:22:51.568816', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 1.82, 'avg_val': 46.141667, 'max_val': 71.72, 'sum_val': 276.85, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 13.005556, 'max_val': 28.88, 'sum_val': 117.05, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 25.576667, 'max_val': 43.83, 'sum_val': 153.46, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 05:11:51.293253', 'min_val': 1.55, 'avg_val': 56.041429, 'max_val': 88.75, 'sum_val': 392.29, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 20:44:47.240204', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 15.736667, 'max_val': 35.06, 'sum_val': 47.21, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 18:29:51.961220', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 24.78, 'avg_val': 61.8125, 'max_val': 99.06, 'sum_val': 494.5, 'row_count': 8},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 13:40:52.394269', 'max_ts': '2022-03-15 15:48:52.007537', 'min_val': 27.15, 'avg_val': 70.535714, 'max_val': 95.03, 'sum_val': 493.75, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 20.495714, 'max_val': 33.91, 'sum_val': 143.47, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:49:51.597689', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 32.85, 'avg_val': 51.452, 'max_val': 79.41, 'sum_val': 257.26, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.187143, 'max_val': 35.91, 'sum_val': 148.31, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 0.59, 'avg_val': 40.327778, 'max_val': 99.51, 'sum_val': 362.95, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 11.09, 'avg_val': 21.4075, 'max_val': 34.85, 'sum_val': 85.63, 'row_count': 4},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:41:46.852459', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 24.838333, 'max_val': 42.67, 'sum_val': 298.06, 'row_count': 12},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:23:51.991431', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 15.063333, 'max_val': 32.88, 'sum_val': 45.19, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 13:14:51.301151', 'max_ts': '2022-03-15 17:10:51.290693', 'min_val': 12.18, 'avg_val': 67.954, 'max_val': 97.21, 'sum_val': 339.77, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 16:48:47.529411', 'min_val': 26.34, 'avg_val': 36.6475, 'max_val': 47.44, 'sum_val': 146.59, 'row_count': 4},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 8.41, 'avg_val': 24.956667, 'max_val': 37.41, 'sum_val': 74.87, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 21.76, 'avg_val': 41.247143, 'max_val': 81.46, 'sum_val': 288.73, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 32.25, 'avg_val': 63.985, 'max_val': 97.07, 'sum_val': 383.91, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 3.79, 'avg_val': 34.408, 'max_val': 46.62, 'sum_val': 172.04, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:21:46.368161', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.22, 'avg_val': 2.676667, 'max_val': 5.57, 'sum_val': 16.06, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:18:51.620244', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 3.14, 'avg_val': 55.120909, 'max_val': 97.33, 'sum_val': 606.33, 'row_count': 11},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 13:15:51.298228', 'max_ts': '2022-03-15 16:09:51.965420', 'min_val': 5.81, 'avg_val': 50.57, 'max_val': 74.43, 'sum_val': 455.13, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 4.748889, 'max_val': 7.88, 'sum_val': 42.74, 'row_count': 9},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:59:52.366762', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 32.09625, 'max_val': 72.75, 'sum_val': 256.77, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 5.444545, 'max_val': 10.93, 'sum_val': 59.89, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 4.838333, 'max_val': 10.45, 'sum_val': 29.03, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 04:32:51.259444', 'min_val': 9.3, 'avg_val': 64.251667, 'max_val': 91.26, 'sum_val': 385.51, 'row_count': 6}]

        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 15.64, 'avg_val': 65.038571, 'max_val': 93.39, 'sum_val': 455.27, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 1.15, 'max_val': 1.96, 'sum_val': 5.75, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.4, 'avg_val': 1.764, 'max_val': 2.32, 'sum_val': 8.82, 'row_count': 5},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 3.34, 'avg_val': 37.635, 'max_val': 75.29, 'sum_val': 150.54, 'row_count': 4},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 15:20:51.252355', 'min_val': 2.17, 'avg_val': 46.666667, 'max_val': 83.23, 'sum_val': 280.0, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 1.772857, 'max_val': 2.88, 'sum_val': 12.41, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:28:52.706334', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 29.35, 'avg_val': 73.844, 'max_val': 97.55, 'sum_val': 369.22, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:38:47.550949', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.33, 'avg_val': 1.867143, 'max_val': 3.01, 'sum_val': 13.07, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 05:11:51.293253', 'min_val': 1.55, 'avg_val': 56.041429, 'max_val': 88.75, 'sum_val': 392.29, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 25.576667, 'max_val': 43.83, 'sum_val': 153.46, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 13.005556, 'max_val': 28.88, 'sum_val': 117.05, 'row_count': 9},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:22:51.568816', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 1.82, 'avg_val': 46.141667, 'max_val': 71.72, 'sum_val': 276.85, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 16:58:51.988529', 'min_val': 9.09, 'avg_val': 46.774286, 'max_val': 92.11, 'sum_val': 327.42, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 20.29625, 'max_val': 45.9, 'sum_val': 162.37, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 21.28625, 'max_val': 37.14, 'sum_val': 170.29, 'row_count': 8},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 22:16:51.251066', 'max_ts': '2022-03-15 22:33:51.964121', 'min_val': 77.11, 'avg_val': 80.705, 'max_val': 84.3, 'sum_val': 161.41, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 11.09, 'avg_val': 21.4075, 'max_val': 34.85, 'sum_val': 85.63, 'row_count': 4},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 0.59, 'avg_val': 40.327778, 'max_val': 99.51, 'sum_val': 362.95, 'row_count': 9},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.187143, 'max_val': 35.91, 'sum_val': 148.31, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:49:51.597689', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 32.85, 'avg_val': 51.452, 'max_val': 79.41, 'sum_val': 257.26, 'row_count': 5},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 20.495714, 'max_val': 33.91, 'sum_val': 143.47, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 13:40:52.394269', 'max_ts': '2022-03-15 15:48:52.007537', 'min_val': 27.15, 'avg_val': 70.535714, 'max_val': 95.03, 'sum_val': 493.75, 'row_count': 7},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 18:29:51.961220', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 24.78, 'avg_val': 61.8125, 'max_val': 99.06, 'sum_val': 494.5, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 20:44:47.240204', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 15.736667, 'max_val': 35.06, 'sum_val': 47.21, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 3.79, 'avg_val': 34.408, 'max_val': 46.62, 'sum_val': 172.04, 'row_count': 5},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 32.25, 'avg_val': 63.985, 'max_val': 97.07, 'sum_val': 383.91, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 21.76, 'avg_val': 41.247143, 'max_val': 81.46, 'sum_val': 288.73, 'row_count': 7},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 8.41, 'avg_val': 24.956667, 'max_val': 37.41, 'sum_val': 74.87, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 16:48:47.529411', 'min_val': 26.34, 'avg_val': 36.6475, 'max_val': 47.44, 'sum_val': 146.59, 'row_count': 4},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 13:14:51.301151', 'max_ts': '2022-03-15 17:10:51.290693', 'min_val': 12.18, 'avg_val': 67.954, 'max_val': 97.21, 'sum_val': 339.77, 'row_count': 5},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:23:51.991431', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 15.063333, 'max_val': 32.88, 'sum_val': 45.19, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:41:46.852459', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 24.838333, 'max_val': 42.67, 'sum_val': 298.06, 'row_count': 12},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 04:32:51.259444', 'min_val': 9.3, 'avg_val': 64.251667, 'max_val': 91.26, 'sum_val': 385.51, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 4.838333, 'max_val': 10.45, 'sum_val': 29.03, 'row_count': 6},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 5.444545, 'max_val': 10.93, 'sum_val': 59.89, 'row_count': 11},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:59:52.366762', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 32.09625, 'max_val': 72.75, 'sum_val': 256.77, 'row_count': 8},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 4.748889, 'max_val': 7.88, 'sum_val': 42.74, 'row_count': 9},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 13:15:51.298228', 'max_ts': '2022-03-15 16:09:51.965420', 'min_val': 5.81, 'avg_val': 50.57, 'max_val': 74.43, 'sum_val': 455.13, 'row_count': 9},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:18:51.620244', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 3.14, 'avg_val': 55.120909, 'max_val': 97.33, 'sum_val': 606.33, 'row_count': 11},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:21:46.368161', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.22, 'avg_val': 2.676667, 'max_val': 5.57, 'sum_val': 16.06, 'row_count': 6}]

        assert asc_result != desc_result

    def test_increments_1hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY min_ts, device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 00:07:46.412776', 'min_val': 11.09, 'avg_val': 11.09, 'max_val': 11.09, 'sum_val': 11.09, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 00:16:51.264448', 'min_val': 15.64, 'avg_val': 38.525, 'max_val': 61.41, 'sum_val': 77.05, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 00:24:52.741697', 'min_val': 88.73, 'avg_val': 89.39, 'max_val': 90.05, 'sum_val': 178.78, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 00:30:47.203906', 'min_val': 42.32, 'avg_val': 42.32, 'max_val': 42.32, 'sum_val': 42.32, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 00:31:51.300486', 'min_val': 57.47, 'avg_val': 57.47, 'max_val': 57.47, 'sum_val': 57.47, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 00:48:46.094775', 'min_val': 31.1, 'avg_val': 34.495, 'max_val': 37.89, 'sum_val': 68.99, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 00:47:52.708401', 'min_val': 64.87, 'avg_val': 64.87, 'max_val': 64.87, 'sum_val': 64.87, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:01:52.374418', 'max_ts': '2022-03-15 01:01:52.374418', 'min_val': 74.3, 'avg_val': 74.3, 'max_val': 74.3, 'sum_val': 74.3, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 01:03:52.002521', 'max_ts': '2022-03-15 01:25:51.611726', 'min_val': 38.21, 'avg_val': 68.86, 'max_val': 99.51, 'sum_val': 137.72, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:17:51.617884', 'max_ts': '2022-03-15 01:17:51.617884', 'min_val': 86.63, 'avg_val': 86.63, 'max_val': 86.63, 'sum_val': 86.63, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 01:20:47.517355', 'min_val': 1.96, 'avg_val': 1.96, 'max_val': 1.96, 'sum_val': 1.96, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:35:46.077756', 'max_ts': '2022-03-15 01:35:46.077756', 'min_val': 35.49, 'avg_val': 35.49, 'max_val': 35.49, 'sum_val': 35.49, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:48:46.391864', 'max_ts': '2022-03-15 01:48:46.391864', 'min_val': 10.59, 'avg_val': 10.59, 'max_val': 10.59, 'sum_val': 10.59, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 01:51:51.251381', 'min_val': 75.88, 'avg_val': 75.88, 'max_val': 75.88, 'sum_val': 75.88, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 01:59:52.742330', 'max_ts': '2022-03-15 01:59:52.742330', 'min_val': 73.41, 'avg_val': 73.41, 'max_val': 73.41, 'sum_val': 73.41, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 02:09:52.726882', 'max_ts': '2022-03-15 02:26:52.005439', 'min_val': 19.14, 'avg_val': 52.63, 'max_val': 73.43, 'sum_val': 157.89, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:10:46.426915', 'max_ts': '2022-03-15 02:10:46.426915', 'min_val': 34.85, 'avg_val': 34.85, 'max_val': 34.85, 'sum_val': 34.85, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:13:51.283861', 'max_ts': '2022-03-15 02:30:52.394622', 'min_val': 0.59, 'avg_val': 28.83, 'max_val': 57.07, 'sum_val': 57.66, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:13:51.985790', 'max_ts': '2022-03-15 02:13:51.985790', 'min_val': 91.26, 'avg_val': 91.26, 'max_val': 91.26, 'sum_val': 91.26, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:18:51.970511', 'max_ts': '2022-03-15 02:18:51.970511', 'min_val': 59.42, 'avg_val': 59.42, 'max_val': 59.42, 'sum_val': 59.42, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:25:46.414598', 'max_ts': '2022-03-15 02:49:47.525052', 'min_val': 0.78, 'avg_val': 1.09, 'max_val': 1.43, 'sum_val': 3.27, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 02:28:47.202760', 'min_val': 5.26, 'avg_val': 5.26, 'max_val': 5.26, 'sum_val': 5.26, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 03:00:47.514114', 'max_ts': '2022-03-15 03:00:47.514114', 'min_val': 43.83, 'avg_val': 43.83, 'max_val': 43.83, 'sum_val': 43.83, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:08:51.600535', 'max_ts': '2022-03-15 03:08:51.600535', 'min_val': 9.3, 'avg_val': 9.3, 'max_val': 9.3, 'sum_val': 9.3, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:10:46.809962', 'max_ts': '2022-03-15 03:45:47.201256', 'min_val': 0.0, 'avg_val': 5.225, 'max_val': 10.45, 'sum_val': 10.45, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 03:24:51.285076', 'max_ts': '2022-03-15 03:24:51.285076', 'min_val': 55.57, 'avg_val': 55.57, 'max_val': 55.57, 'sum_val': 55.57, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 03:36:51.960578', 'max_ts': '2022-03-15 03:43:51.575814', 'min_val': 21.35, 'avg_val': 45.605, 'max_val': 69.86, 'sum_val': 91.21, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:02:46.852845', 'max_ts': '2022-03-15 04:19:46.423049', 'min_val': 3.79, 'avg_val': 23.805, 'max_val': 43.82, 'sum_val': 47.61, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:07:52.002847', 'max_ts': '2022-03-15 04:07:52.002847', 'min_val': 32.25, 'avg_val': 32.25, 'max_val': 32.25, 'sum_val': 32.25, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:17:46.083077', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 2.15, 'avg_val': 4.44, 'max_val': 5.71, 'sum_val': 13.32, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:32:51.259444', 'max_ts': '2022-03-15 04:32:51.259444', 'min_val': 32.76, 'avg_val': 32.76, 'max_val': 32.76, 'sum_val': 32.76, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:50:52.716817', 'max_ts': '2022-03-15 04:50:52.716817', 'min_val': 87.52, 'avg_val': 87.52, 'max_val': 87.52, 'sum_val': 87.52, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:55:46.778730', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 0.52, 'max_val': 0.52, 'sum_val': 0.52, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 04:55:52.709587', 'max_ts': '2022-03-15 04:55:52.709587', 'min_val': 1.55, 'avg_val': 1.55, 'max_val': 1.55, 'sum_val': 1.55, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:07:51.281096', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 4.82, 'avg_val': 5.745, 'max_val': 6.67, 'sum_val': 11.49, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:11:51.293253', 'max_ts': '2022-03-15 05:11:51.293253', 'min_val': 88.75, 'avg_val': 88.75, 'max_val': 88.75, 'sum_val': 88.75, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:15:46.075339', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 14.03, 'avg_val': 19.845, 'max_val': 25.66, 'sum_val': 39.69, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:34:52.706622', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 44.83, 'avg_val': 73.403333, 'max_val': 97.07, 'sum_val': 220.21, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:37:47.564979', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 46.62, 'avg_val': 46.62, 'max_val': 46.62, 'sum_val': 46.62, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 05:43:52.758682', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 63.59, 'avg_val': 78.49, 'max_val': 93.39, 'sum_val': 156.98, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:44:47.238599', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 15.025, 'max_val': 28.0, 'sum_val': 30.05, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 06:17:46.736484', 'min_val': 23.63, 'avg_val': 24.34, 'max_val': 25.05, 'sum_val': 48.68, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:22:51.568816', 'max_ts': '2022-03-15 06:47:51.985033', 'min_val': 1.82, 'avg_val': 36.68, 'max_val': 71.54, 'sum_val': 73.36, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 06:32:47.541993', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 06:32:51.960105', 'min_val': 21.76, 'avg_val': 21.76, 'max_val': 21.76, 'sum_val': 21.76, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 07:22:46.370373', 'min_val': 1.55, 'avg_val': 1.89, 'max_val': 2.23, 'sum_val': 3.78, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 07:05:46.374750', 'min_val': 29.05, 'avg_val': 29.05, 'max_val': 29.05, 'sum_val': 29.05, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 07:05:51.614800', 'min_val': 3.34, 'avg_val': 3.34, 'max_val': 3.34, 'sum_val': 3.34, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 07:08:46.415135', 'max_ts': '2022-03-15 07:08:46.415135', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:17:52.374609', 'max_ts': '2022-03-15 07:17:52.374609', 'min_val': 47.35, 'avg_val': 47.35, 'max_val': 47.35, 'sum_val': 47.35, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 07:24:46.073295', 'min_val': 15.66, 'avg_val': 15.66, 'max_val': 15.66, 'sum_val': 15.66, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:49:51.597689', 'max_ts': '2022-03-15 07:49:51.597689', 'min_val': 38.8, 'avg_val': 38.8, 'max_val': 38.8, 'sum_val': 38.8, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:59:52.366762', 'max_ts': '2022-03-15 07:59:52.366762', 'min_val': 35.61, 'avg_val': 35.61, 'max_val': 35.61, 'sum_val': 35.61, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 08:00:46.829341', 'max_ts': '2022-03-15 08:56:46.421889', 'min_val': 0.5, 'avg_val': 6.258333, 'max_val': 10.93, 'sum_val': 37.55, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 08:01:51.567086', 'max_ts': '2022-03-15 08:01:51.567086', 'min_val': 2.57, 'avg_val': 2.57, 'max_val': 2.57, 'sum_val': 2.57, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:17:47.516724', 'max_ts': '2022-03-15 08:17:47.516724', 'min_val': 8.41, 'avg_val': 8.41, 'max_val': 8.41, 'sum_val': 8.41, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:19:47.239243', 'max_ts': '2022-03-15 08:19:47.239243', 'min_val': 23.59, 'avg_val': 23.59, 'max_val': 23.59, 'sum_val': 23.59, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 08:20:47.522034', 'max_ts': '2022-03-15 08:20:47.522034', 'min_val': 2.15, 'avg_val': 2.15, 'max_val': 2.15, 'sum_val': 2.15, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:25:51.996538', 'max_ts': '2022-03-15 08:33:52.409299', 'min_val': 25.17, 'avg_val': 32.185, 'max_val': 39.2, 'sum_val': 64.37, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:33:52.715460', 'max_ts': '2022-03-15 08:33:52.715460', 'min_val': 58.01, 'avg_val': 58.01, 'max_val': 58.01, 'sum_val': 58.01, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 09:06:52.762716', 'max_ts': '2022-03-15 09:34:52.366909', 'min_val': 3.65, 'avg_val': 39.47, 'max_val': 75.29, 'sum_val': 78.94, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:18:47.531564', 'max_ts': '2022-03-15 09:18:47.531564', 'min_val': 2.56, 'avg_val': 2.56, 'max_val': 2.56, 'sum_val': 2.56, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:20:51.999518', 'max_ts': '2022-03-15 09:20:51.999518', 'min_val': 32.85, 'avg_val': 32.85, 'max_val': 32.85, 'sum_val': 32.85, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:23:47.517655', 'max_ts': '2022-03-15 09:29:46.401743', 'min_val': 10.21, 'avg_val': 14.59, 'max_val': 18.97, 'sum_val': 29.18, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:28:51.266267', 'max_ts': '2022-03-15 09:31:52.385871', 'min_val': 61.83, 'avg_val': 66.775, 'max_val': 71.72, 'sum_val': 133.55, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:34:52.408369', 'max_ts': '2022-03-15 09:34:52.408369', 'min_val': 47.3, 'avg_val': 47.3, 'max_val': 47.3, 'sum_val': 47.3, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 09:35:51.288727', 'max_ts': '2022-03-15 09:52:52.417781', 'min_val': 18.89, 'avg_val': 41.13, 'max_val': 63.37, 'sum_val': 82.26, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:47:47.222903', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 37.41, 'avg_val': 37.41, 'max_val': 37.41, 'sum_val': 37.41, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:15:46.824028', 'max_ts': '2022-03-15 10:58:47.221547', 'min_val': 0.19, 'avg_val': 14.8, 'max_val': 28.88, 'sum_val': 59.2, 'row_count': 4},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:19:47.240814', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 26.626667, 'max_val': 35.91, 'sum_val': 79.88, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:24:51.283426', 'max_ts': '2022-03-15 10:24:51.283426', 'min_val': 48.19, 'avg_val': 48.19, 'max_val': 48.19, 'sum_val': 48.19, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 10:33:51.964373', 'max_ts': '2022-03-15 10:57:51.585040', 'min_val': 8.7, 'avg_val': 29.145, 'max_val': 49.59, 'sum_val': 58.29, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 10:36:47.549483', 'max_ts': '2022-03-15 10:50:47.518579', 'min_val': 1.42, 'avg_val': 1.87, 'max_val': 2.32, 'sum_val': 3.74, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:43:51.275489', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 67.37, 'avg_val': 67.37, 'max_val': 67.37, 'sum_val': 67.37, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:00:52.009794', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 26.87, 'max_val': 72.75, 'sum_val': 80.61, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 11:02:46.104113', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 5.21, 'avg_val': 5.21, 'max_val': 5.21, 'sum_val': 5.21, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:07:47.528947', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 1.87, 'avg_val': 6.186667, 'max_val': 8.71, 'sum_val': 18.56, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 11:12:51.580880', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 26.49, 'avg_val': 53.975, 'max_val': 81.46, 'sum_val': 107.95, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:19:46.732823', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.53, 'avg_val': 1.53, 'max_val': 1.53, 'sum_val': 1.53, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:35:51.260707', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 68.26, 'avg_val': 68.26, 'max_val': 68.26, 'sum_val': 68.26, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 11:40:51.581152', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 79.41, 'avg_val': 79.41, 'max_val': 79.41, 'sum_val': 79.41, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 12:04:46.781482', 'min_val': 0.1, 'avg_val': 0.1, 'max_val': 0.1, 'sum_val': 0.1, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 12:50:52.707432', 'min_val': 9.09, 'avg_val': 54.663333, 'max_val': 92.11, 'sum_val': 163.99, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 12:42:51.304342', 'min_val': 23.97, 'avg_val': 46.77, 'max_val': 69.57, 'sum_val': 93.54, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 12:38:46.067345', 'min_val': 6.81, 'avg_val': 6.81, 'max_val': 6.81, 'sum_val': 6.81, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 12:45:47.224260', 'min_val': 26.34, 'avg_val': 26.34, 'max_val': 26.34, 'sum_val': 26.34, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 12:50:46.731418', 'min_val': 33.91, 'avg_val': 33.91, 'max_val': 33.91, 'sum_val': 33.91, 'row_count': 1}]

        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 12:42:51.304342', 'min_val': 23.97, 'avg_val': 46.77, 'max_val': 69.57, 'sum_val': 93.54, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:35:51.260707', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 68.26, 'avg_val': 68.26, 'max_val': 68.26, 'sum_val': 68.26, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:19:46.732823', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.53, 'avg_val': 1.53, 'max_val': 1.53, 'sum_val': 1.53, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 10:36:47.549483', 'max_ts': '2022-03-15 10:50:47.518579', 'min_val': 1.42, 'avg_val': 1.87, 'max_val': 2.32, 'sum_val': 3.74, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 09:06:52.762716', 'max_ts': '2022-03-15 09:34:52.366909', 'min_val': 3.65, 'avg_val': 39.47, 'max_val': 75.29, 'sum_val': 78.94, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 08:20:47.522034', 'max_ts': '2022-03-15 08:20:47.522034', 'min_val': 2.15, 'avg_val': 2.15, 'max_val': 2.15, 'sum_val': 2.15, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 07:05:51.614800', 'min_val': 3.34, 'avg_val': 3.34, 'max_val': 3.34, 'sum_val': 3.34, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 06:32:47.541993', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 05:43:52.758682', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 63.59, 'avg_val': 78.49, 'max_val': 93.39, 'sum_val': 156.98, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:55:46.778730', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 0.52, 'max_val': 0.52, 'sum_val': 0.52, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:50:52.716817', 'max_ts': '2022-03-15 04:50:52.716817', 'min_val': 87.52, 'avg_val': 87.52, 'max_val': 87.52, 'sum_val': 87.52, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:25:46.414598', 'max_ts': '2022-03-15 02:49:47.525052', 'min_val': 0.78, 'avg_val': 1.09, 'max_val': 1.43, 'sum_val': 3.27, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:18:51.970511', 'max_ts': '2022-03-15 02:18:51.970511', 'min_val': 59.42, 'avg_val': 59.42, 'max_val': 59.42, 'sum_val': 59.42, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 01:20:47.517355', 'min_val': 1.96, 'avg_val': 1.96, 'max_val': 1.96, 'sum_val': 1.96, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:01:52.374418', 'max_ts': '2022-03-15 01:01:52.374418', 'min_val': 74.3, 'avg_val': 74.3, 'max_val': 74.3, 'sum_val': 74.3, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 00:16:51.264448', 'min_val': 15.64, 'avg_val': 38.525, 'max_val': 61.41, 'sum_val': 77.05, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 12:38:46.067345', 'min_val': 6.81, 'avg_val': 6.81, 'max_val': 6.81, 'sum_val': 6.81, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 12:50:52.707432', 'min_val': 9.09, 'avg_val': 54.663333, 'max_val': 92.11, 'sum_val': 163.99, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 11:02:46.104113', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 5.21, 'avg_val': 5.21, 'max_val': 5.21, 'sum_val': 5.21, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:43:51.275489', 'max_ts': '2022-03-15 10:43:51.275489', 'min_val': 67.37, 'avg_val': 67.37, 'max_val': 67.37, 'sum_val': 67.37, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:15:46.824028', 'max_ts': '2022-03-15 10:58:47.221547', 'min_val': 0.19, 'avg_val': 14.8, 'max_val': 28.88, 'sum_val': 59.2, 'row_count': 4},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:28:51.266267', 'max_ts': '2022-03-15 09:31:52.385871', 'min_val': 61.83, 'avg_val': 66.775, 'max_val': 71.72, 'sum_val': 133.55, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:18:47.531564', 'max_ts': '2022-03-15 09:18:47.531564', 'min_val': 2.56, 'avg_val': 2.56, 'max_val': 2.56, 'sum_val': 2.56, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 08:01:51.567086', 'max_ts': '2022-03-15 08:01:51.567086', 'min_val': 2.57, 'avg_val': 2.57, 'max_val': 2.57, 'sum_val': 2.57, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 07:08:46.415135', 'max_ts': '2022-03-15 07:08:46.415135', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:22:51.568816', 'max_ts': '2022-03-15 06:47:51.985033', 'min_val': 1.82, 'avg_val': 36.68, 'max_val': 71.54, 'sum_val': 73.36, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 06:17:46.736484', 'min_val': 23.63, 'avg_val': 24.34, 'max_val': 25.05, 'sum_val': 48.68, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:44:47.238599', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 15.025, 'max_val': 28.0, 'sum_val': 30.05, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:11:51.293253', 'max_ts': '2022-03-15 05:11:51.293253', 'min_val': 88.75, 'avg_val': 88.75, 'max_val': 88.75, 'sum_val': 88.75, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 04:55:52.709587', 'max_ts': '2022-03-15 04:55:52.709587', 'min_val': 1.55, 'avg_val': 1.55, 'max_val': 1.55, 'sum_val': 1.55, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 03:00:47.514114', 'max_ts': '2022-03-15 03:00:47.514114', 'min_val': 43.83, 'avg_val': 43.83, 'max_val': 43.83, 'sum_val': 43.83, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 02:09:52.726882', 'max_ts': '2022-03-15 02:26:52.005439', 'min_val': 19.14, 'avg_val': 52.63, 'max_val': 73.43, 'sum_val': 157.89, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:48:46.391864', 'max_ts': '2022-03-15 01:48:46.391864', 'min_val': 10.59, 'avg_val': 10.59, 'max_val': 10.59, 'sum_val': 10.59, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:17:51.617884', 'max_ts': '2022-03-15 01:17:51.617884', 'min_val': 86.63, 'avg_val': 86.63, 'max_val': 86.63, 'sum_val': 86.63, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 00:48:46.094775', 'min_val': 31.1, 'avg_val': 34.495, 'max_val': 37.89, 'sum_val': 68.99, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 00:31:51.300486', 'min_val': 57.47, 'avg_val': 57.47, 'max_val': 57.47, 'sum_val': 57.47, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 12:50:46.731418', 'min_val': 33.91, 'avg_val': 33.91, 'max_val': 33.91, 'sum_val': 33.91, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 11:40:51.581152', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 79.41, 'avg_val': 79.41, 'max_val': 79.41, 'sum_val': 79.41, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:24:51.283426', 'max_ts': '2022-03-15 10:24:51.283426', 'min_val': 48.19, 'avg_val': 48.19, 'max_val': 48.19, 'sum_val': 48.19, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:19:47.240814', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 26.626667, 'max_val': 35.91, 'sum_val': 79.88, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:23:47.517655', 'max_ts': '2022-03-15 09:29:46.401743', 'min_val': 10.21, 'avg_val': 14.59, 'max_val': 18.97, 'sum_val': 29.18, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:20:51.999518', 'max_ts': '2022-03-15 09:20:51.999518', 'min_val': 32.85, 'avg_val': 32.85, 'max_val': 32.85, 'sum_val': 32.85, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:33:52.715460', 'max_ts': '2022-03-15 08:33:52.715460', 'min_val': 58.01, 'avg_val': 58.01, 'max_val': 58.01, 'sum_val': 58.01, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:19:47.239243', 'max_ts': '2022-03-15 08:19:47.239243', 'min_val': 23.59, 'avg_val': 23.59, 'max_val': 23.59, 'sum_val': 23.59, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:49:51.597689', 'max_ts': '2022-03-15 07:49:51.597689', 'min_val': 38.8, 'avg_val': 38.8, 'max_val': 38.8, 'sum_val': 38.8, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 07:24:46.073295', 'min_val': 15.66, 'avg_val': 15.66, 'max_val': 15.66, 'sum_val': 15.66, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:15:46.075339', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 14.03, 'avg_val': 19.845, 'max_val': 25.66, 'sum_val': 39.69, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:07:51.281096', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 4.82, 'avg_val': 5.745, 'max_val': 6.67, 'sum_val': 11.49, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 03:36:51.960578', 'max_ts': '2022-03-15 03:43:51.575814', 'min_val': 21.35, 'avg_val': 45.605, 'max_val': 69.86, 'sum_val': 91.21, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:13:51.283861', 'max_ts': '2022-03-15 02:30:52.394622', 'min_val': 0.59, 'avg_val': 28.83, 'max_val': 57.07, 'sum_val': 57.66, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:10:46.426915', 'max_ts': '2022-03-15 02:10:46.426915', 'min_val': 34.85, 'avg_val': 34.85, 'max_val': 34.85, 'sum_val': 34.85, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 01:03:52.002521', 'max_ts': '2022-03-15 01:25:51.611726', 'min_val': 38.21, 'avg_val': 68.86, 'max_val': 99.51, 'sum_val': 137.72, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:47:52.708401', 'max_ts': '2022-03-15 00:47:52.708401', 'min_val': 64.87, 'avg_val': 64.87, 'max_val': 64.87, 'sum_val': 64.87, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 00:07:46.412776', 'min_val': 11.09, 'avg_val': 11.09, 'max_val': 11.09, 'sum_val': 11.09, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 12:45:47.224260', 'min_val': 26.34, 'avg_val': 26.34, 'max_val': 26.34, 'sum_val': 26.34, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 11:12:51.580880', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 26.49, 'avg_val': 53.975, 'max_val': 81.46, 'sum_val': 107.95, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:47:47.222903', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 37.41, 'avg_val': 37.41, 'max_val': 37.41, 'sum_val': 37.41, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:34:52.408369', 'max_ts': '2022-03-15 09:34:52.408369', 'min_val': 47.3, 'avg_val': 47.3, 'max_val': 47.3, 'sum_val': 47.3, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:25:51.996538', 'max_ts': '2022-03-15 08:33:52.409299', 'min_val': 25.17, 'avg_val': 32.185, 'max_val': 39.2, 'sum_val': 64.37, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:17:47.516724', 'max_ts': '2022-03-15 08:17:47.516724', 'min_val': 8.41, 'avg_val': 8.41, 'max_val': 8.41, 'sum_val': 8.41, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:17:52.374609', 'max_ts': '2022-03-15 07:17:52.374609', 'min_val': 47.35, 'avg_val': 47.35, 'max_val': 47.35, 'sum_val': 47.35, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 07:05:46.374750', 'min_val': 29.05, 'avg_val': 29.05, 'max_val': 29.05, 'sum_val': 29.05, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 06:32:51.960105', 'min_val': 21.76, 'avg_val': 21.76, 'max_val': 21.76, 'sum_val': 21.76, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:37:47.564979', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 46.62, 'avg_val': 46.62, 'max_val': 46.62, 'sum_val': 46.62, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:34:52.706622', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 44.83, 'avg_val': 73.403333, 'max_val': 97.07, 'sum_val': 220.21, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:07:52.002847', 'max_ts': '2022-03-15 04:07:52.002847', 'min_val': 32.25, 'avg_val': 32.25, 'max_val': 32.25, 'sum_val': 32.25, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:02:46.852845', 'max_ts': '2022-03-15 04:19:46.423049', 'min_val': 3.79, 'avg_val': 23.805, 'max_val': 43.82, 'sum_val': 47.61, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 03:24:51.285076', 'max_ts': '2022-03-15 03:24:51.285076', 'min_val': 55.57, 'avg_val': 55.57, 'max_val': 55.57, 'sum_val': 55.57, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:51:51.251381', 'max_ts': '2022-03-15 01:51:51.251381', 'min_val': 75.88, 'avg_val': 75.88, 'max_val': 75.88, 'sum_val': 75.88, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:35:46.077756', 'max_ts': '2022-03-15 01:35:46.077756', 'min_val': 35.49, 'avg_val': 35.49, 'max_val': 35.49, 'sum_val': 35.49, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 00:30:47.203906', 'min_val': 42.32, 'avg_val': 42.32, 'max_val': 42.32, 'sum_val': 42.32, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 12:04:46.781482', 'min_val': 0.1, 'avg_val': 0.1, 'max_val': 0.1, 'sum_val': 0.1, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:07:47.528947', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 1.87, 'avg_val': 6.186667, 'max_val': 8.71, 'sum_val': 18.56, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:00:52.009794', 'max_ts': '2022-03-15 11:45:51.280173', 'min_val': 0.91, 'avg_val': 26.87, 'max_val': 72.75, 'sum_val': 80.61, 'row_count': 3},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 10:33:51.964373', 'max_ts': '2022-03-15 10:57:51.585040', 'min_val': 8.7, 'avg_val': 29.145, 'max_val': 49.59, 'sum_val': 58.29, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 09:35:51.288727', 'max_ts': '2022-03-15 09:52:52.417781', 'min_val': 18.89, 'avg_val': 41.13, 'max_val': 63.37, 'sum_val': 82.26, 'row_count': 2},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 08:00:46.829341', 'max_ts': '2022-03-15 08:56:46.421889', 'min_val': 0.5, 'avg_val': 6.258333, 'max_val': 10.93, 'sum_val': 37.55, 'row_count': 6},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:59:52.366762', 'max_ts': '2022-03-15 07:59:52.366762', 'min_val': 35.61, 'avg_val': 35.61, 'max_val': 35.61, 'sum_val': 35.61, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 07:22:46.370373', 'min_val': 1.55, 'avg_val': 1.89, 'max_val': 2.23, 'sum_val': 3.78, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:32:51.259444', 'max_ts': '2022-03-15 04:32:51.259444', 'min_val': 32.76, 'avg_val': 32.76, 'max_val': 32.76, 'sum_val': 32.76, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:17:46.083077', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 2.15, 'avg_val': 4.44, 'max_val': 5.71, 'sum_val': 13.32, 'row_count': 3},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:10:46.809962', 'max_ts': '2022-03-15 03:45:47.201256', 'min_val': 0.0, 'avg_val': 5.225, 'max_val': 10.45, 'sum_val': 10.45, 'row_count': 2},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:08:51.600535', 'max_ts': '2022-03-15 03:08:51.600535', 'min_val': 9.3, 'avg_val': 9.3, 'max_val': 9.3, 'sum_val': 9.3, 'row_count': 1},
                          {'table': 'ping_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 02:28:47.202760', 'min_val': 5.26, 'avg_val': 5.26, 'max_val': 5.26, 'sum_val': 5.26, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:13:51.985790', 'max_ts': '2022-03-15 02:13:51.985790', 'min_val': 91.26, 'avg_val': 91.26, 'max_val': 91.26, 'sum_val': 91.26, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 01:59:52.742330', 'max_ts': '2022-03-15 01:59:52.742330', 'min_val': 73.41, 'avg_val': 73.41, 'max_val': 73.41, 'sum_val': 73.41, 'row_count': 1},
                          {'table': 'percentagecpu_sensor', 'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 00:24:52.741697', 'min_val': 88.73, 'avg_val': 89.39, 'max_val': 90.05, 'sum_val': 178.78, 'row_count': 2}]

        assert desc_result != asc_result

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
        query = (self.base_query + ' "SELECT increments(day, 30, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\'"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.896316, 'max_val': 49.0, 'sum_val': 31888.01, 'row_count': 2006},
                          {'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.0, 'avg_val': 14.893007, 'max_val': 48.98, 'sum_val': 59095.45, 'row_count': 3968},
                          {'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.640228, 'max_val': 48.87, 'sum_val': 3850.38, 'row_count': 263},
                          {'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.01, 'avg_val': 15.118887, 'max_val': 49.0, 'sum_val': 32052.04, 'row_count': 2120}]

    def test_increments_15day(self):
        query = (self.base_query + ' "SELECT increments(day, 15, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-05-01 00:00:00\' AND timestamp >= \'2022-02-01 00:00:00\' '
                +'ORDER BY min_ts ASC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-14 23:35:47.507093', 'min_val': 0.5, 'avg_val': 18.513462, 'max_val': 48.2, 'sum_val': 1444.05, 'row_count': 78},
                          {'min_ts': '2022-02-15 00:01:46.048094', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.0, 'avg_val': 15.790436, 'max_val': 49.0, 'sum_val': 30443.96, 'row_count': 1928},
                          {'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-14 23:43:46.381074', 'min_val': 0.0, 'avg_val': 15.156264, 'max_val': 48.98, 'sum_val': 29251.59, 'row_count': 1930},
                          {'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.0, 'avg_val': 14.6437, 'max_val': 48.96, 'sum_val': 29843.86, 'row_count': 2038},
                          {'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.640228, 'max_val': 48.87, 'sum_val': 3850.38, 'row_count': 263},
                          {'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-14 23:40:47.530353', 'min_val': 0.01, 'avg_val': 15.195459, 'max_val': 49.0, 'sum_val': 29281.65, 'row_count': 1927},
                          {'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.03, 'avg_val': 14.354352, 'max_val': 46.38, 'sum_val': 2770.39, 'row_count': 193}]

    def test_increments_7day(self):
        query = (self.base_query + ' "SELECT increments(day, 7, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-01 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 14.606992, 'max_val': 48.87, 'sum_val': 7332.71, 'row_count': 502},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.01, 'avg_val': 14.447417, 'max_val': 48.84, 'sum_val': 13985.1, 'row_count': 968},
                          {'min_ts': '2022-03-14 00:14:46.735774', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 14.854756, 'max_val': 48.96, 'sum_val': 14305.13, 'row_count': 963},
                          {'min_ts': '2022-03-07 00:19:46.056837', 'max_ts': '2022-03-13 23:57:47.233039', 'min_val': 0.01, 'avg_val': 14.727345, 'max_val': 48.97, 'sum_val': 13755.34, 'row_count': 934},
                          {'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-06 23:40:47.544449', 'min_val': 0.0, 'avg_val': 15.703183, 'max_val': 48.98, 'sum_val': 13567.55, 'row_count': 864}]

    def test_increments_1day(self):
        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.06, 'avg_val': 15.841374, 'max_val': 48.87, 'sum_val': 2075.22, 'row_count': 131},
                          {'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-30 23:37:46.062928', 'min_val': 0.02, 'avg_val': 13.448182, 'max_val': 46.87, 'sum_val': 1775.16, 'row_count': 132},
                          {'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.15, 'avg_val': 14.937521, 'max_val': 47.8, 'sum_val': 1747.69, 'row_count': 117},
                          {'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 14.218361, 'max_val': 45.29, 'sum_val': 1734.64, 'row_count': 122},
                          {'min_ts': '2022-03-27 00:06:47.542971', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 14.212721, 'max_val': 48.84, 'sum_val': 2089.27, 'row_count': 147},
                          {'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 14.736443, 'max_val': 48.06, 'sum_val': 2195.73, 'row_count': 149},
                          {'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 15.347482, 'max_val': 47.1, 'sum_val': 2133.3, 'row_count': 139},
                          {'min_ts': '2022-03-24 00:36:46.074681', 'max_ts': '2022-03-24 23:26:47.195182', 'min_val': 0.01, 'avg_val': 13.136797, 'max_val': 48.29, 'sum_val': 1681.51, 'row_count': 128},
                          {'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 13.265349, 'max_val': 48.45, 'sum_val': 1711.23, 'row_count': 129},
                          {'min_ts': '2022-03-22 00:09:46.389923', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 14.310621, 'max_val': 43.64, 'sum_val': 2075.04, 'row_count': 145},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:33:46.385868', 'min_val': 0.04, 'avg_val': 16.023053, 'max_val': 47.44, 'sum_val': 2099.02, 'row_count': 131},
                          {'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 13.752963, 'max_val': 48.96, 'sum_val': 1856.65, 'row_count': 135},
                          {'min_ts': '2022-03-19 00:08:46.092527', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 15.034155, 'max_val': 48.05, 'sum_val': 2134.85, 'row_count': 142},
                          {'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 13.823231, 'max_val': 48.87, 'sum_val': 1797.02, 'row_count': 130},
                          {'min_ts': '2022-03-17 00:08:47.216280', 'max_ts': '2022-03-17 23:53:47.507880', 'min_val': 0.21, 'avg_val': 16.661135, 'max_val': 48.87, 'sum_val': 2349.22, 'row_count': 141},
                          {'min_ts': '2022-03-16 00:09:46.068468', 'max_ts': '2022-03-16 23:56:47.244853', 'min_val': 0.03, 'avg_val': 15.440861, 'max_val': 48.07, 'sum_val': 2331.57, 'row_count': 151},
                          {'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 0.0, 'avg_val': 14.447879, 'max_val': 47.44, 'sum_val': 1907.12, 'row_count': 132}]

        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert asc_result == [{'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 0.0, 'avg_val': 14.447879, 'max_val': 47.44, 'sum_val': 1907.12, 'row_count': 132},
                          {'min_ts': '2022-03-16 00:09:46.068468', 'max_ts': '2022-03-16 23:56:47.244853', 'min_val': 0.03, 'avg_val': 15.440861, 'max_val': 48.07, 'sum_val': 2331.57, 'row_count': 151},
                          {'min_ts': '2022-03-17 00:08:47.216280', 'max_ts': '2022-03-17 23:53:47.507880', 'min_val': 0.21, 'avg_val': 16.661135, 'max_val': 48.87, 'sum_val': 2349.22, 'row_count': 141},
                          {'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 13.823231, 'max_val': 48.87, 'sum_val': 1797.02, 'row_count': 130},
                          {'min_ts': '2022-03-19 00:08:46.092527', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 15.034155, 'max_val': 48.05, 'sum_val': 2134.85, 'row_count': 142},
                          {'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 13.752963, 'max_val': 48.96, 'sum_val': 1856.65, 'row_count': 135},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:33:46.385868', 'min_val': 0.04, 'avg_val': 16.023053, 'max_val': 47.44, 'sum_val': 2099.02, 'row_count': 131},
                          {'min_ts': '2022-03-22 00:09:46.389923', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 14.310621, 'max_val': 43.64, 'sum_val': 2075.04, 'row_count': 145},
                          {'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 13.265349, 'max_val': 48.45, 'sum_val': 1711.23, 'row_count': 129},
                          {'min_ts': '2022-03-24 00:36:46.074681', 'max_ts': '2022-03-24 23:26:47.195182', 'min_val': 0.01, 'avg_val': 13.136797, 'max_val': 48.29, 'sum_val': 1681.51, 'row_count': 128},
                          {'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 15.347482, 'max_val': 47.1, 'sum_val': 2133.3, 'row_count': 139},
                          {'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 14.736443, 'max_val': 48.06, 'sum_val': 2195.73, 'row_count': 149},
                          {'min_ts': '2022-03-27 00:06:47.542971', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 14.212721, 'max_val': 48.84, 'sum_val': 2089.27, 'row_count': 147},
                          {'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 14.218361, 'max_val': 45.29, 'sum_val': 1734.64, 'row_count': 122},
                          {'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.15, 'avg_val': 14.937521, 'max_val': 47.8, 'sum_val': 1747.69, 'row_count': 117},
                          {'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-30 23:37:46.062928', 'min_val': 0.02, 'avg_val': 13.448182, 'max_val': 46.87, 'sum_val': 1775.16, 'row_count': 132},
                          {'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.06, 'avg_val': 15.841374, 'max_val': 48.87, 'sum_val': 2075.22, 'row_count': 131}]

        assert asc_result != desc_result

    def test_increments_12hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 5.230588, 'max_val': 10.93, 'sum_val': 88.92, 'row_count': 17},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.1, 'avg_val': 3.92, 'max_val': 7.88, 'sum_val': 58.8, 'row_count': 15},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 3.79, 'avg_val': 30.86375, 'max_val': 46.62, 'sum_val': 246.91, 'row_count': 8},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 27.790625, 'max_val': 47.44, 'sum_val': 444.65, 'row_count': 16},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.267273, 'max_val': 35.91, 'sum_val': 233.94, 'row_count': 11},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 19.068, 'max_val': 35.06, 'sum_val': 190.68, 'row_count': 10},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 18.034, 'max_val': 43.83, 'sum_val': 270.51, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 20.79125, 'max_val': 45.9, 'sum_val': 332.66, 'row_count': 16},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 0.52, 'avg_val': 1.457, 'max_val': 2.32, 'sum_val': 14.57, 'row_count': 10},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.21, 'avg_val': 1.82, 'max_val': 3.01, 'sum_val': 25.48, 'row_count': 14}]

        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)
        assert asc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 0.52, 'avg_val': 1.457, 'max_val': 2.32, 'sum_val': 14.57, 'row_count': 10},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.21, 'avg_val': 1.82, 'max_val': 3.01, 'sum_val': 25.48, 'row_count': 14},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 18.034, 'max_val': 43.83, 'sum_val': 270.51, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 20.79125, 'max_val': 45.9, 'sum_val': 332.66, 'row_count': 16},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.267273, 'max_val': 35.91, 'sum_val': 233.94, 'row_count': 11},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 19.068, 'max_val': 35.06, 'sum_val': 190.68, 'row_count': 10},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 3.79, 'avg_val': 30.86375, 'max_val': 46.62, 'sum_val': 246.91, 'row_count': 8},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 27.790625, 'max_val': 47.44, 'sum_val': 444.65, 'row_count': 16},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 5.230588, 'max_val': 10.93, 'sum_val': 88.92, 'row_count': 17},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.1, 'avg_val': 3.92, 'max_val': 7.88, 'sum_val': 58.8, 'row_count': 15}]

        assert asc_result != desc_result

    def test_increments_6hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:38:47.550949', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.33, 'avg_val': 1.867143, 'max_val': 3.01, 'sum_val': 13.07, 'row_count': 7},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 1.772857, 'max_val': 2.88, 'sum_val': 12.41, 'row_count': 7},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.4, 'avg_val': 1.764, 'max_val': 2.32, 'sum_val': 8.82, 'row_count': 5},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 1.15, 'max_val': 1.96, 'sum_val': 5.75, 'row_count': 5},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 21.28625, 'max_val': 37.14, 'sum_val': 170.29, 'row_count': 8},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 20.29625, 'max_val': 45.9, 'sum_val': 162.37, 'row_count': 8},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 13.005556, 'max_val': 28.88, 'sum_val': 117.05, 'row_count': 9},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 25.576667, 'max_val': 43.83, 'sum_val': 153.46, 'row_count': 6},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 20:44:47.240204', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 15.736667, 'max_val': 35.06, 'sum_val': 47.21, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 20.495714, 'max_val': 33.91, 'sum_val': 143.47, 'row_count': 7},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.187143, 'max_val': 35.91, 'sum_val': 148.31, 'row_count': 7},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 11.09, 'avg_val': 21.4075, 'max_val': 34.85, 'sum_val': 85.63, 'row_count': 4},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:41:46.852459', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 24.838333, 'max_val': 42.67, 'sum_val': 298.06, 'row_count': 12},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 16:48:47.529411', 'min_val': 26.34, 'avg_val': 36.6475, 'max_val': 47.44, 'sum_val': 146.59, 'row_count': 4},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 8.41, 'avg_val': 24.956667, 'max_val': 37.41, 'sum_val': 74.87, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 3.79, 'avg_val': 34.408, 'max_val': 46.62, 'sum_val': 172.04, 'row_count': 5},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:21:46.368161', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.22, 'avg_val': 2.676667, 'max_val': 5.57, 'sum_val': 16.06, 'row_count': 6},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 4.748889, 'max_val': 7.88, 'sum_val': 42.74, 'row_count': 9},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 5.444545, 'max_val': 10.93, 'sum_val': 59.89, 'row_count': 11},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 4.838333, 'max_val': 10.45, 'sum_val': 29.03, 'row_count': 6}]

        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 1.15, 'max_val': 1.96, 'sum_val': 5.75, 'row_count': 5},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.4, 'avg_val': 1.764, 'max_val': 2.32, 'sum_val': 8.82, 'row_count': 5},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 13:27:47.536992', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 1.772857, 'max_val': 2.88, 'sum_val': 12.41, 'row_count': 7},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:38:47.550949', 'max_ts': '2022-03-15 23:29:47.228486', 'min_val': 0.33, 'avg_val': 1.867143, 'max_val': 3.01, 'sum_val': 13.07, 'row_count': 7},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 25.576667, 'max_val': 43.83, 'sum_val': 153.46, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 13.005556, 'max_val': 28.88, 'sum_val': 117.05, 'row_count': 9},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 20.29625, 'max_val': 45.9, 'sum_val': 162.37, 'row_count': 8},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 21.28625, 'max_val': 37.14, 'sum_val': 170.29, 'row_count': 8},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 11.09, 'avg_val': 21.4075, 'max_val': 34.85, 'sum_val': 85.63, 'row_count': 4},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 21.187143, 'max_val': 35.91, 'sum_val': 148.31, 'row_count': 7},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 20.495714, 'max_val': 33.91, 'sum_val': 143.47, 'row_count': 7},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 20:44:47.240204', 'max_ts': '2022-03-15 21:53:47.513692', 'min_val': 3.22, 'avg_val': 15.736667, 'max_val': 35.06, 'sum_val': 47.21, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 3.79, 'avg_val': 34.408, 'max_val': 46.62, 'sum_val': 172.04, 'row_count': 5},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 8.41, 'avg_val': 24.956667, 'max_val': 37.41, 'sum_val': 74.87, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 16:48:47.529411', 'min_val': 26.34, 'avg_val': 36.6475, 'max_val': 47.44, 'sum_val': 146.59, 'row_count': 4},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:41:46.852459', 'max_ts': '2022-03-15 23:31:46.097974', 'min_val': 6.86, 'avg_val': 24.838333, 'max_val': 42.67, 'sum_val': 298.06, 'row_count': 12},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 4.838333, 'max_val': 10.45, 'sum_val': 29.03, 'row_count': 6},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 5.444545, 'max_val': 10.93, 'sum_val': 59.89, 'row_count': 11},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 4.748889, 'max_val': 7.88, 'sum_val': 42.74, 'row_count': 9},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:21:46.368161', 'max_ts': '2022-03-15 22:14:46.396593', 'min_val': 0.22, 'avg_val': 2.676667, 'max_val': 5.57, 'sum_val': 16.06, 'row_count': 6}]

        assert asc_result != desc_result

    def test_increments_1hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY min_ts, device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 00:07:46.412776', 'min_val': 11.09, 'avg_val': 11.09, 'max_val': 11.09, 'sum_val': 11.09, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 00:30:47.203906', 'min_val': 42.32, 'avg_val': 42.32, 'max_val': 42.32, 'sum_val': 42.32, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:39:46.083225', 'max_ts': '2022-03-15 00:48:46.094775', 'min_val': 31.1, 'avg_val': 34.495, 'max_val': 37.89, 'sum_val': 68.99, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:20:47.517355', 'max_ts': '2022-03-15 01:20:47.517355', 'min_val': 1.96, 'avg_val': 1.96, 'max_val': 1.96, 'sum_val': 1.96, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:35:46.077756', 'max_ts': '2022-03-15 01:35:46.077756', 'min_val': 35.49, 'avg_val': 35.49, 'max_val': 35.49, 'sum_val': 35.49, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:48:46.391864', 'max_ts': '2022-03-15 01:48:46.391864', 'min_val': 10.59, 'avg_val': 10.59, 'max_val': 10.59, 'sum_val': 10.59, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:10:46.426915', 'max_ts': '2022-03-15 02:10:46.426915', 'min_val': 34.85, 'avg_val': 34.85, 'max_val': 34.85, 'sum_val': 34.85, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:25:46.414598', 'max_ts': '2022-03-15 02:49:47.525052', 'min_val': 0.78, 'avg_val': 1.09, 'max_val': 1.43, 'sum_val': 3.27, 'row_count': 3},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:28:47.202760', 'max_ts': '2022-03-15 02:28:47.202760', 'min_val': 5.26, 'avg_val': 5.26, 'max_val': 5.26, 'sum_val': 5.26, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 03:00:47.514114', 'max_ts': '2022-03-15 03:00:47.514114', 'min_val': 43.83, 'avg_val': 43.83, 'max_val': 43.83, 'sum_val': 43.83, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:10:46.809962', 'max_ts': '2022-03-15 03:45:47.201256', 'min_val': 0.0, 'avg_val': 5.225, 'max_val': 10.45, 'sum_val': 10.45, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:02:46.852845', 'max_ts': '2022-03-15 04:19:46.423049', 'min_val': 3.79, 'avg_val': 23.805, 'max_val': 43.82, 'sum_val': 47.61, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:17:46.083077', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 2.15, 'avg_val': 4.44, 'max_val': 5.71, 'sum_val': 13.32, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:55:46.778730', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 0.52, 'max_val': 0.52, 'sum_val': 0.52, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:15:46.075339', 'max_ts': '2022-03-15 05:18:46.057246', 'min_val': 14.03, 'avg_val': 19.845, 'max_val': 25.66, 'sum_val': 39.69, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:37:47.564979', 'max_ts': '2022-03-15 05:37:47.564979', 'min_val': 46.62, 'avg_val': 46.62, 'max_val': 46.62, 'sum_val': 46.62, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:44:47.238599', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 15.025, 'max_val': 28.0, 'sum_val': 30.05, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 06:17:46.736484', 'min_val': 23.63, 'avg_val': 24.34, 'max_val': 25.05, 'sum_val': 48.68, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 06:32:47.541993', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 07:22:46.370373', 'min_val': 1.55, 'avg_val': 1.89, 'max_val': 2.23, 'sum_val': 3.78, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 07:05:46.374750', 'min_val': 29.05, 'avg_val': 29.05, 'max_val': 29.05, 'sum_val': 29.05, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 07:08:46.415135', 'max_ts': '2022-03-15 07:08:46.415135', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 07:24:46.073295', 'min_val': 15.66, 'avg_val': 15.66, 'max_val': 15.66, 'sum_val': 15.66, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 08:00:46.829341', 'max_ts': '2022-03-15 08:56:46.421889', 'min_val': 0.5, 'avg_val': 6.258333, 'max_val': 10.93, 'sum_val': 37.55, 'row_count': 6},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:17:47.516724', 'max_ts': '2022-03-15 08:17:47.516724', 'min_val': 8.41, 'avg_val': 8.41, 'max_val': 8.41, 'sum_val': 8.41, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:19:47.239243', 'max_ts': '2022-03-15 08:19:47.239243', 'min_val': 23.59, 'avg_val': 23.59, 'max_val': 23.59, 'sum_val': 23.59, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 08:20:47.522034', 'max_ts': '2022-03-15 08:20:47.522034', 'min_val': 2.15, 'avg_val': 2.15, 'max_val': 2.15, 'sum_val': 2.15, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:18:47.531564', 'max_ts': '2022-03-15 09:18:47.531564', 'min_val': 2.56, 'avg_val': 2.56, 'max_val': 2.56, 'sum_val': 2.56, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:23:47.517655', 'max_ts': '2022-03-15 09:29:46.401743', 'min_val': 10.21, 'avg_val': 14.59, 'max_val': 18.97, 'sum_val': 29.18, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:47:47.222903', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 37.41, 'avg_val': 37.41, 'max_val': 37.41, 'sum_val': 37.41, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:15:46.824028', 'max_ts': '2022-03-15 10:58:47.221547', 'min_val': 0.19, 'avg_val': 14.8, 'max_val': 28.88, 'sum_val': 59.2, 'row_count': 4},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:19:47.240814', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 26.626667, 'max_val': 35.91, 'sum_val': 79.88, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 10:36:47.549483', 'max_ts': '2022-03-15 10:50:47.518579', 'min_val': 1.42, 'avg_val': 1.87, 'max_val': 2.32, 'sum_val': 3.74, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 11:02:46.104113', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 5.21, 'avg_val': 5.21, 'max_val': 5.21, 'sum_val': 5.21, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:07:47.528947', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 1.87, 'avg_val': 6.186667, 'max_val': 8.71, 'sum_val': 18.56, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:19:46.732823', 'max_ts': '2022-03-15 11:19:46.732823', 'min_val': 1.53, 'avg_val': 1.53, 'max_val': 1.53, 'sum_val': 1.53, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 12:04:46.781482', 'min_val': 0.1, 'avg_val': 0.1, 'max_val': 0.1, 'sum_val': 0.1, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:38:46.067345', 'max_ts': '2022-03-15 12:38:46.067345', 'min_val': 6.81, 'avg_val': 6.81, 'max_val': 6.81, 'sum_val': 6.81, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 12:45:47.224260', 'min_val': 26.34, 'avg_val': 26.34, 'max_val': 26.34, 'sum_val': 26.34, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 12:50:46.731418', 'min_val': 33.91, 'avg_val': 33.91, 'max_val': 33.91, 'sum_val': 33.91, 'row_count': 1}]

        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert desc_result != asc_result

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

    def test_increments_1month(self):
        query = (self.base_query + ' "SELECT increments(month, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\' GROUP BY device_name"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-28 23:34:46.063492', 'min_val': 0.0, 'avg_val': 25.696322, 'max_val': 99.72, 'sum_val': 20891.11, 'row_count': 813},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-02-13 21:58:46.378304', 'max_ts': '2022-02-28 22:39:51.589780', 'min_val': 0.0, 'avg_val': 39.094366, 'max_val': 99.94, 'sum_val': 31431.87, 'row_count': 804},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-02-13 22:09:46.053613', 'max_ts': '2022-02-28 23:39:47.519260', 'min_val': 0.02, 'avg_val': 34.854959, 'max_val': 99.84, 'sum_val': 30010.12, 'row_count': 861},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.05, 'avg_val': 38.081612, 'max_val': 99.43, 'sum_val': 32369.37, 'row_count': 850},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-02-13 22:06:52.719775', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.02, 'avg_val': 28.406398, 'max_val': 99.55, 'sum_val': 21844.52, 'row_count': 769},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-01 00:35:51.289448', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.0, 'avg_val': 25.963829, 'max_val': 99.91, 'sum_val': 43800.98, 'row_count': 1687},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-01 00:30:46.096552', 'max_ts': '2022-03-31 22:20:46.755617', 'min_val': 0.03, 'avg_val': 36.202691, 'max_val': 99.87, 'sum_val': 61073.94, 'row_count': 1687},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-31 23:41:51.303285', 'min_val': 0.47, 'avg_val': 36.353614, 'max_val': 99.94, 'sum_val': 61655.73, 'row_count': 1696},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-01 00:07:46.084507', 'max_ts': '2022-03-31 22:54:46.059694', 'min_val': 0.19, 'avg_val': 37.85591, 'max_val': 99.9, 'sum_val': 64052.2, 'row_count': 1692},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-01 00:05:46.393130', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.0, 'avg_val': 28.204835, 'max_val': 99.59, 'sum_val': 49584.1, 'row_count': 1758},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-16 19:49:52.012942', 'min_val': 0.0, 'avg_val': 25.963809, 'max_val': 99.99, 'sum_val': 23107.79, 'row_count': 890},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 0.17, 'avg_val': 38.110391, 'max_val': 99.83, 'sum_val': 32127.06, 'row_count': 843},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-16 19:35:51.596377', 'min_val': 1.64, 'avg_val': 35.305658, 'max_val': 99.91, 'sum_val': 29515.53, 'row_count': 836},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-04-01 00:18:52.374500', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.07, 'avg_val': 37.164385, 'max_val': 99.52, 'sum_val': 32630.33, 'row_count': 878},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 16:12:52.398129', 'min_val': 0.03, 'avg_val': 28.685698, 'max_val': 99.96, 'sum_val': 25071.3, 'row_count': 874}]

    def test_increments_30day(self):
        query = (self.base_query + ' "SELECT increments(day, 30, timestamp), webid, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-12-31 23:59:59\' GROUP BY webid"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw', 'min_ts': '2022-02-13 21:58:46.378304', 'max_ts': '2022-02-28 22:39:51.589780', 'min_val': 0.0, 'avg_val': 39.094366, 'max_val': 99.94, 'sum_val': 31431.87, 'row_count': 804},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H', 'min_ts': '2022-02-13 22:09:46.053613', 'max_ts': '2022-02-28 23:39:47.519260', 'min_val': 0.02, 'avg_val': 34.854959, 'max_val': 99.84, 'sum_val': 30010.12, 'row_count': 861},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H', 'min_ts': '2022-02-13 22:06:52.719775', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.02, 'avg_val': 28.406398, 'max_val': 99.55, 'sum_val': 21844.52, 'row_count': 769},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-28 23:34:46.063492', 'min_val': 0.0, 'avg_val': 25.696322, 'max_val': 99.72, 'sum_val': 20891.11, 'row_count': 813},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.05, 'avg_val': 38.081612, 'max_val': 99.43, 'sum_val': 32369.37, 'row_count': 850},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw', 'min_ts': '2022-03-01 00:30:46.096552', 'max_ts': '2022-03-29 23:26:51.263819', 'min_val': 0.03, 'avg_val': 36.339191, 'max_val': 99.87, 'sum_val': 57961.01, 'row_count': 1595},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-29 23:14:47.514567', 'min_val': 0.47, 'avg_val': 36.407551, 'max_val': 99.94, 'sum_val': 57232.67, 'row_count': 1572},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H', 'min_ts': '2022-03-01 00:05:46.393130', 'max_ts': '2022-03-29 23:38:47.226700', 'min_val': 0.0, 'avg_val': 27.992103, 'max_val': 99.59, 'sum_val': 46578.86, 'row_count': 1664},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H', 'min_ts': '2022-03-01 00:35:51.289448', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.0, 'avg_val': 25.935271, 'max_val': 99.91, 'sum_val': 40744.31, 'row_count': 1571},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw', 'min_ts': '2022-03-01 00:07:46.084507', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.19, 'avg_val': 37.812131, 'max_val': 99.9, 'sum_val': 59970.04, 'row_count': 1586},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw', 'min_ts': '2022-03-30 00:45:46.761087', 'max_ts': '2022-03-31 22:20:46.755617', 'min_val': 0.29, 'avg_val': 33.836196, 'max_val': 96.74, 'sum_val': 3112.93, 'row_count': 92},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-31 23:41:51.303285', 'min_val': 1.49, 'avg_val': 35.669839, 'max_val': 99.41, 'sum_val': 4423.06, 'row_count': 124},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H', 'min_ts': '2022-03-30 01:36:47.522643', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.14, 'avg_val': 31.970638, 'max_val': 98.7, 'sum_val': 3005.24, 'row_count': 94},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 26.350603, 'max_val': 99.5, 'sum_val': 3056.67, 'row_count': 116},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw', 'min_ts': '2022-03-30 00:12:51.588889', 'max_ts': '2022-03-31 22:54:46.059694', 'min_val': 0.85, 'avg_val': 38.510943, 'max_val': 98.47, 'sum_val': 4082.16, 'row_count': 106},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70A74uuaOGS6RG0ZdSFZFT0ug4FckGTrxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxDQVRBTFlTVCAzNTAwWEx8UElORw', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 0.17, 'avg_val': 38.110391, 'max_val': 99.83, 'sum_val': 32127.06, 'row_count': 843},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AMgi98B6o6hG0bdSFZFT0ugPdQ3gcXLd1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xHT09HTEVfUElOR3xQSU5H', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-16 19:35:51.596377', 'min_val': 1.64, 'avg_val': 35.305658, 'max_val': 99.91, 'sum_val': 29515.53, 'row_count': 836},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70ATrGzGrGT6RG0ZdSFZFT0ugQW05a2rwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxGLk8gTU9OSVRPUklORyBTRVJWRVJcVk0gTElUIFNMIE5NU3xQSU5H', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-16 16:12:52.398129', 'min_val': 0.03, 'avg_val': 28.685698, 'max_val': 99.96, 'sum_val': 25071.3, 'row_count': 874},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70AkxjnYuCS6RG0ZdSFZFT0ugnMRtEzvxdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBRFZBIEZTUDMwMDBSN3xQSU5H', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-16 19:49:52.012942', 'min_val': 0.0, 'avg_val': 25.963809, 'max_val': 99.99, 'sum_val': 23107.79, 'row_count': 890},
                          {'webid': 'F1AbEfLbwwL8F6EiShvDV-QH70Ay9wV1b5Y6hG0bdSFZFT0ugxACfpGU7d1ojPpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxVQklRVUlUSSBPTFR8UElORw', 'min_ts': '2022-04-01 00:18:52.374500', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 0.07, 'avg_val': 37.164385, 'max_val': 99.52, 'sum_val': 32630.33, 'row_count': 878}]

    def test_increments_15day(self):
        query = (self.base_query + ' "SELECT increments(day, 15, timestamp), parentelement, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-05-01 00:00:00\' AND timestamp >= \'2022-02-01 00:00:00\' GROUP BY parentelement '
                +'ORDER BY min_ts ASC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-13 21:20:51.999012', 'max_ts': '2022-02-14 22:50:46.395025', 'min_val': 0.5, 'avg_val': 26.760833, 'max_val': 94.34, 'sum_val': 642.26, 'row_count': 24},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-13 21:21:46.746294', 'max_ts': '2022-02-14 23:52:52.755470', 'min_val': 4.18, 'avg_val': 40.964286, 'max_val': 97.38, 'sum_val': 1433.75, 'row_count': 35},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-13 21:58:46.378304', 'max_ts': '2022-02-14 22:32:51.593645', 'min_val': 2.73, 'avg_val': 36.632593, 'max_val': 86.46, 'sum_val': 989.08, 'row_count': 27},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-13 22:06:52.719775', 'max_ts': '2022-02-14 22:37:51.961332', 'min_val': 0.83, 'avg_val': 25.886176, 'max_val': 99.55, 'sum_val': 880.13, 'row_count': 34},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-13 22:09:46.053613', 'max_ts': '2022-02-14 23:55:51.296406', 'min_val': 2.66, 'avg_val': 36.176667, 'max_val': 96.14, 'sum_val': 1302.36, 'row_count': 36},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-15 00:01:46.048094', 'max_ts': '2022-02-28 23:43:46.851381', 'min_val': 0.05, 'avg_val': 37.957816, 'max_val': 99.43, 'sum_val': 30935.62, 'row_count': 815},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-02-15 00:04:46.734543', 'max_ts': '2022-02-28 23:39:47.519260', 'min_val': 0.02, 'avg_val': 34.797285, 'max_val': 99.84, 'sum_val': 28707.76, 'row_count': 825},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-15 00:05:52.386039', 'max_ts': '2022-02-28 23:34:46.063492', 'min_val': 0.0, 'avg_val': 25.663942, 'max_val': 99.72, 'sum_val': 20248.85, 'row_count': 789},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-15 00:08:47.536007', 'max_ts': '2022-02-28 23:31:51.286046', 'min_val': 0.02, 'avg_val': 28.52298, 'max_val': 99.41, 'sum_val': 20964.39, 'row_count': 735},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-02-15 00:18:52.379300', 'max_ts': '2022-02-28 22:39:51.589780', 'min_val': 0.0, 'avg_val': 39.17991, 'max_val': 99.94, 'sum_val': 30442.79, 'row_count': 777},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-14 22:58:51.611428', 'min_val': 0.52, 'avg_val': 36.128502, 'max_val': 99.27, 'sum_val': 29914.4, 'row_count': 828},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-01 00:05:46.393130', 'max_ts': '2022-03-14 23:43:46.381074', 'min_val': 0.0, 'avg_val': 26.65867, 'max_val': 99.59, 'sum_val': 20047.32, 'row_count': 752},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-01 00:07:46.084507', 'max_ts': '2022-03-14 23:46:52.004831', 'min_val': 0.2, 'avg_val': 38.187127, 'max_val': 99.5, 'sum_val': 28182.1, 'row_count': 738},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-01 00:30:46.096552', 'max_ts': '2022-03-14 23:22:51.270059', 'min_val': 0.03, 'avg_val': 36.608852, 'max_val': 99.87, 'sum_val': 29653.17, 'row_count': 810},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-01 00:35:51.289448', 'max_ts': '2022-03-14 23:00:52.013109', 'min_val': 0.01, 'avg_val': 25.373912, 'max_val': 99.63, 'sum_val': 19005.06, 'row_count': 749},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-29 23:14:47.514567', 'min_val': 0.47, 'avg_val': 36.718105, 'max_val': 99.94, 'sum_val': 27318.27, 'row_count': 744},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.0, 'avg_val': 26.446776, 'max_val': 99.91, 'sum_val': 21739.25, 'row_count': 822},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-29 23:38:47.226700', 'min_val': 0.0, 'avg_val': 29.091601, 'max_val': 99.16, 'sum_val': 26531.54, 'row_count': 912},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-29 23:45:46.050793', 'min_val': 0.19, 'avg_val': 37.485778, 'max_val': 99.9, 'sum_val': 31787.94, 'row_count': 848},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-29 23:26:51.263819', 'min_val': 0.15, 'avg_val': 36.060943, 'max_val': 99.64, 'sum_val': 28307.84, 'row_count': 785},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-31 23:41:51.303285', 'min_val': 1.49, 'avg_val': 35.669839, 'max_val': 99.41, 'sum_val': 4423.06, 'row_count': 124},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-30 00:04:46.074385', 'max_ts': '2022-03-31 23:59:47.556256', 'min_val': 0.02, 'avg_val': 26.350603, 'max_val': 99.5, 'sum_val': 3056.67, 'row_count': 116},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-03-30 00:12:51.588889', 'max_ts': '2022-03-31 22:54:46.059694', 'min_val': 0.85, 'avg_val': 38.510943, 'max_val': 98.47, 'sum_val': 4082.16, 'row_count': 106},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-30 00:45:46.761087', 'max_ts': '2022-03-31 22:20:46.755617', 'min_val': 0.29, 'avg_val': 33.836196, 'max_val': 96.74, 'sum_val': 3112.93, 'row_count': 92},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-03-30 01:36:47.522643', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.14, 'avg_val': 31.970638, 'max_val': 98.7, 'sum_val': 3005.24, 'row_count': 94},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:06:51.275824', 'max_ts': '2022-04-14 23:35:46.425955', 'min_val': 0.0, 'avg_val': 25.900574, 'max_val': 99.99, 'sum_val': 20746.36, 'row_count': 801},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:07:46.844366', 'max_ts': '2022-04-14 23:17:46.103727', 'min_val': 0.03, 'avg_val': 29.080911, 'max_val': 99.96, 'sum_val': 23293.81, 'row_count': 801},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-01 00:17:46.837569', 'max_ts': '2022-04-14 23:23:51.264121', 'min_val': 0.17, 'avg_val': 37.783885, 'max_val': 99.6, 'sum_val': 28980.24, 'row_count': 767},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 00:18:52.374500', 'max_ts': '2022-04-14 23:40:47.530353', 'min_val': 0.07, 'avg_val': 37.40847, 'max_val': 99.52, 'sum_val': 30076.41, 'row_count': 804},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-01 00:29:46.391348', 'max_ts': '2022-04-14 23:45:51.249043', 'min_val': 1.64, 'avg_val': 35.356574, 'max_val': 99.91, 'sum_val': 26835.64, 'row_count': 759},
                          {'parentelement': 'd515dccb-58be-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:01:46.743220', 'max_ts': '2022-04-16 20:33:46.370019', 'min_val': 2.06, 'avg_val': 34.512432, 'max_val': 95.05, 'sum_val': 2553.92, 'row_count': 74},
                          {'parentelement': '1ab3b14e-93b1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:09:46.421460', 'max_ts': '2022-04-16 16:12:52.398129', 'min_val': 0.03, 'avg_val': 24.349178, 'max_val': 89.33, 'sum_val': 1777.49, 'row_count': 73},
                          {'parentelement': '68ae8bef-92e1-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:10:47.518961', 'max_ts': '2022-04-16 20:09:52.725939', 'min_val': 2.94, 'avg_val': 41.405526, 'max_val': 99.83, 'sum_val': 3146.82, 'row_count': 76},
                          {'parentelement': 'f0bd0832-a81e-11ea-b46d-d4856454f4ba', 'min_ts': '2022-04-15 00:22:52.417430', 'max_ts': '2022-04-16 19:35:51.596377', 'min_val': 5.23, 'avg_val': 34.803766, 'max_val': 99.8, 'sum_val': 2679.89, 'row_count': 77},
                          {'parentelement': '62e71893-92e0-11e9-b465-d4856454f4ba', 'min_ts': '2022-04-15 00:45:51.620001', 'max_ts': '2022-04-16 19:49:52.012942', 'min_val': 0.04, 'avg_val': 26.532921, 'max_val': 98.03, 'sum_val': 2361.43, 'row_count': 89}]


    def test_increments_7day(self):
        query = (self.base_query + ' "SELECT increments(day, 7, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-01 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert result == [{'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.02, 'avg_val': 32.705302, 'max_val': 99.5, 'sum_val': 33555.64, 'row_count': 1026},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.01, 'avg_val': 33.621711, 'max_val': 99.94, 'sum_val': 65427.85, 'row_count': 1946},
                          {'min_ts': '2022-03-14 00:13:51.291886', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 32.406071, 'max_val': 99.9, 'sum_val': 63256.65, 'row_count': 1952},
                          {'min_ts': '2022-03-07 00:01:51.971909', 'max_ts': '2022-03-13 23:57:47.233039', 'min_val': 0.01, 'avg_val': 32.642258, 'max_val': 99.87, 'sum_val': 61726.51, 'row_count': 1891},
                          {'min_ts': '2022-03-01 00:02:46.063795', 'max_ts': '2022-03-06 23:59:51.992156', 'min_val': 0.0, 'avg_val': 32.962053, 'max_val': 99.74, 'sum_val': 56200.3, 'row_count': 1705}]

    def test_increments_1day(self):
        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.06, 'avg_val': 33.523951, 'max_val': 99.41, 'sum_val': 8146.32, 'row_count': 243},
                          {'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-30 23:59:51.301063', 'min_val': 0.02, 'avg_val': 32.98872, 'max_val': 99.5, 'sum_val': 9533.74, 'row_count': 289},
                          {'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.15, 'avg_val': 32.810496, 'max_val': 98.67, 'sum_val': 7940.14, 'row_count': 242},
                          {'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 31.489841, 'max_val': 99.45, 'sum_val': 7935.44, 'row_count': 252},
                          {'min_ts': '2022-03-27 00:03:51.269763', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 32.277949, 'max_val': 99.77, 'sum_val': 8811.88, 'row_count': 273},
                          {'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 32.092491, 'max_val': 97.64, 'sum_val': 9403.1, 'row_count': 293},
                          {'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 34.574375, 'max_val': 98.19, 'sum_val': 9957.42, 'row_count': 288},
                          {'min_ts': '2022-03-24 00:23:52.386471', 'max_ts': '2022-03-24 23:58:51.277280', 'min_val': 0.01, 'avg_val': 33.94323, 'max_val': 99.94, 'sum_val': 8723.41, 'row_count': 257},
                          {'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 34.640143, 'max_val': 99.64, 'sum_val': 9699.24, 'row_count': 280},
                          {'min_ts': '2022-03-22 00:06:51.619546', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 32.522818, 'max_val': 99.76, 'sum_val': 9464.14, 'row_count': 291},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:52:51.587190', 'min_val': 0.04, 'avg_val': 35.487348, 'max_val': 99.91, 'sum_val': 9368.66, 'row_count': 264},
                          {'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 32.465714, 'max_val': 99.77, 'sum_val': 9317.66, 'row_count': 287},
                          {'min_ts': '2022-03-19 00:00:52.400235', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 31.957256, 'max_val': 96.41, 'sum_val': 8852.16, 'row_count': 277},
                          {'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 33.381601, 'max_val': 99.9, 'sum_val': 9380.23, 'row_count': 281},
                          {'min_ts': '2022-03-17 00:01:51.600314', 'max_ts': '2022-03-17 23:58:52.424868', 'min_val': 0.21, 'avg_val': 32.359314, 'max_val': 98.16, 'sum_val': 8963.53, 'row_count': 277},
                          {'min_ts': '2022-03-16 00:07:52.385601', 'max_ts': '2022-03-16 23:59:51.964092', 'min_val': 0.03, 'avg_val': 31.757474, 'max_val': 97.37, 'sum_val': 9177.91, 'row_count': 289},
                          {'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 0.0, 'avg_val': 33.422769, 'max_val': 99.51, 'sum_val': 8689.92, 'row_count': 260}]

        query = (self.base_query + ' "SELECT increments(day, 1, timestamp), min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp < \'2022-04-01 00:00:00\' AND timestamp >= \'2022-03-15 00:00:00\' '
                +'ORDER BY min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert asc_result == [{'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 0.0, 'avg_val': 33.422769, 'max_val': 99.51, 'sum_val': 8689.92, 'row_count': 260},
                          {'min_ts': '2022-03-16 00:07:52.385601', 'max_ts': '2022-03-16 23:59:51.964092', 'min_val': 0.03, 'avg_val': 31.757474, 'max_val': 97.37, 'sum_val': 9177.91, 'row_count': 289},
                          {'min_ts': '2022-03-17 00:01:51.600314', 'max_ts': '2022-03-17 23:58:52.424868', 'min_val': 0.21, 'avg_val': 32.359314, 'max_val': 98.16, 'sum_val': 8963.53, 'row_count': 277},
                          {'min_ts': '2022-03-18 00:07:47.539833', 'max_ts': '2022-03-18 23:58:47.240727', 'min_val': 0.04, 'avg_val': 33.381601, 'max_val': 99.9, 'sum_val': 9380.23, 'row_count': 281},
                          {'min_ts': '2022-03-19 00:00:52.400235', 'max_ts': '2022-03-19 23:58:46.077818', 'min_val': 0.04, 'avg_val': 31.957256, 'max_val': 96.41, 'sum_val': 8852.16, 'row_count': 277},
                          {'min_ts': '2022-03-20 00:05:46.089521', 'max_ts': '2022-03-20 23:59:46.394995', 'min_val': 0.0, 'avg_val': 32.465714, 'max_val': 99.77, 'sum_val': 9317.66, 'row_count': 287},
                          {'min_ts': '2022-03-21 00:02:46.755646', 'max_ts': '2022-03-21 23:52:51.587190', 'min_val': 0.04, 'avg_val': 35.487348, 'max_val': 99.91, 'sum_val': 9368.66, 'row_count': 264},
                          {'min_ts': '2022-03-22 00:06:51.619546', 'max_ts': '2022-03-22 23:54:47.512431', 'min_val': 0.36, 'avg_val': 32.522818, 'max_val': 99.76, 'sum_val': 9464.14, 'row_count': 291},
                          {'min_ts': '2022-03-23 00:10:46.794589', 'max_ts': '2022-03-23 23:57:46.390147', 'min_val': 0.08, 'avg_val': 34.640143, 'max_val': 99.64, 'sum_val': 9699.24, 'row_count': 280},
                          {'min_ts': '2022-03-24 00:23:52.386471', 'max_ts': '2022-03-24 23:58:51.277280', 'min_val': 0.01, 'avg_val': 33.94323, 'max_val': 99.94, 'sum_val': 8723.41, 'row_count': 257},
                          {'min_ts': '2022-03-25 00:00:46.426887', 'max_ts': '2022-03-25 23:59:46.753408', 'min_val': 0.21, 'avg_val': 34.574375, 'max_val': 98.19, 'sum_val': 9957.42, 'row_count': 288},
                          {'min_ts': '2022-03-26 00:05:46.067529', 'max_ts': '2022-03-26 23:56:46.373225', 'min_val': 0.08, 'avg_val': 32.092491, 'max_val': 97.64, 'sum_val': 9403.1, 'row_count': 293},
                          {'min_ts': '2022-03-27 00:03:51.269763', 'max_ts': '2022-03-27 23:56:47.251533', 'min_val': 0.1, 'avg_val': 32.277949, 'max_val': 99.77, 'sum_val': 8811.88, 'row_count': 273},
                          {'min_ts': '2022-03-28 00:01:46.388103', 'max_ts': '2022-03-28 23:56:47.246604', 'min_val': 0.04, 'avg_val': 31.489841, 'max_val': 99.45, 'sum_val': 7935.44, 'row_count': 252},
                          {'min_ts': '2022-03-29 00:03:46.076087', 'max_ts': '2022-03-29 23:47:52.738979', 'min_val': 0.15, 'avg_val': 32.810496, 'max_val': 98.67, 'sum_val': 7940.14, 'row_count': 242},
                          {'min_ts': '2022-03-30 00:00:51.300215', 'max_ts': '2022-03-30 23:59:51.301063', 'min_val': 0.02, 'avg_val': 32.98872, 'max_val': 99.5, 'sum_val': 9533.74, 'row_count': 289},
                          {'min_ts': '2022-03-31 00:05:46.800249', 'max_ts': '2022-03-31 23:59:52.738132', 'min_val': 0.06, 'avg_val': 33.523951, 'max_val': 99.41, 'sum_val': 8146.32, 'row_count': 243}]

        assert asc_result != desc_result

    def test_increments_12hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 23.587097, 'max_val': 91.26, 'sum_val': 731.2, 'row_count': 31},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 0.1, 'avg_val': 32.007429, 'max_val': 97.33, 'sum_val': 1120.26, 'row_count': 35},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 3.79, 'avg_val': 43.788095, 'max_val': 97.07, 'sum_val': 919.55, 'row_count': 21},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 34.567083, 'max_val': 97.21, 'sum_val': 829.61, 'row_count': 24},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 0.59, 'avg_val': 34.166, 'max_val': 99.51, 'sum_val': 854.15, 'row_count': 25},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 3.22, 'avg_val': 47.1572, 'max_val': 99.06, 'sum_val': 1178.93, 'row_count': 25},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 33.558929, 'max_val': 88.75, 'sum_val': 939.65, 'row_count': 28},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 32.8596, 'max_val': 92.11, 'sum_val': 821.49, 'row_count': 25},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 0.52, 'avg_val': 29.541905, 'max_val': 93.39, 'sum_val': 620.38, 'row_count': 21},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 0.21, 'avg_val': 26.988, 'max_val': 97.55, 'sum_val': 674.7, 'row_count': 25}]

        query = (self.base_query + ' "SELECT increments(hour, 12, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 0.52, 'avg_val': 29.541905, 'max_val': 93.39, 'sum_val': 620.38, 'row_count': 21},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 0.21, 'avg_val': 26.988, 'max_val': 97.55, 'sum_val': 674.7, 'row_count': 25},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 33.558929, 'max_val': 88.75, 'sum_val': 939.65, 'row_count': 28},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 32.8596, 'max_val': 92.11, 'sum_val': 821.49, 'row_count': 25},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 0.59, 'avg_val': 34.166, 'max_val': 99.51, 'sum_val': 854.15, 'row_count': 25},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 3.22, 'avg_val': 47.1572, 'max_val': 99.06, 'sum_val': 1178.93, 'row_count': 25},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 3.79, 'avg_val': 43.788095, 'max_val': 97.07, 'sum_val': 919.55, 'row_count': 21},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 34.567083, 'max_val': 97.21, 'sum_val': 829.61, 'row_count': 24},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.0, 'avg_val': 23.587097, 'max_val': 91.26, 'sum_val': 731.2, 'row_count': 31},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 0.1, 'avg_val': 32.007429, 'max_val': 97.33, 'sum_val': 1120.26, 'row_count': 35}]

        assert asc_result != desc_result

    def test_increments_6hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:28:52.706334', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 0.33, 'avg_val': 31.8575, 'max_val': 97.55, 'sum_val': 382.29, 'row_count': 12},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 22.493077, 'max_val': 83.23, 'sum_val': 292.41, 'row_count': 13},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 1.4, 'avg_val': 17.706667, 'max_val': 75.29, 'sum_val': 159.36, 'row_count': 9},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 0.52, 'avg_val': 38.418333, 'max_val': 93.39, 'sum_val': 461.02, 'row_count': 12},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 33.17, 'max_val': 84.3, 'sum_val': 331.7, 'row_count': 10},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 32.652667, 'max_val': 92.11, 'sum_val': 489.79, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 26.26, 'max_val': 71.72, 'sum_val': 393.9, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 1.55, 'avg_val': 41.980769, 'max_val': 88.75, 'sum_val': 545.75, 'row_count': 13},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 18:29:51.961220', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 3.22, 'avg_val': 49.246364, 'max_val': 99.06, 'sum_val': 541.71, 'row_count': 11},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 45.515714, 'max_val': 95.03, 'sum_val': 637.22, 'row_count': 14},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 8.54, 'avg_val': 33.7975, 'max_val': 79.41, 'sum_val': 405.57, 'row_count': 12},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 0.59, 'avg_val': 34.506154, 'max_val': 99.51, 'sum_val': 448.58, 'row_count': 13},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:23:51.991431', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 22.883333, 'max_val': 42.67, 'sum_val': 343.25, 'row_count': 15},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 17:10:51.290693', 'min_val': 12.18, 'avg_val': 54.04, 'max_val': 97.21, 'sum_val': 486.36, 'row_count': 9},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 8.41, 'avg_val': 36.36, 'max_val': 81.46, 'sum_val': 363.6, 'row_count': 10},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 3.79, 'avg_val': 50.540909, 'max_val': 97.07, 'sum_val': 555.95, 'row_count': 11},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:18:51.620244', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 0.22, 'avg_val': 36.611176, 'max_val': 97.33, 'sum_val': 622.39, 'row_count': 17},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 27.659444, 'max_val': 74.43, 'sum_val': 497.87, 'row_count': 18},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 16.666316, 'max_val': 72.75, 'sum_val': 316.66, 'row_count': 19},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 34.545, 'max_val': 91.26, 'sum_val': 414.54, 'row_count': 12}]

        query = (self.base_query + ' "SELECT increments(hour, 6, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-16 00:00:00\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts ASC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 0.52, 'avg_val': 38.418333, 'max_val': 93.39, 'sum_val': 461.02, 'row_count': 12},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 1.4, 'avg_val': 17.706667, 'max_val': 75.29, 'sum_val': 159.36, 'row_count': 9},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 17:54:46.093330', 'min_val': 0.21, 'avg_val': 22.493077, 'max_val': 83.23, 'sum_val': 292.41, 'row_count': 13},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 19:28:52.706334', 'max_ts': '2022-03-15 23:44:51.966588', 'min_val': 0.33, 'avg_val': 31.8575, 'max_val': 97.55, 'sum_val': 382.29, 'row_count': 12},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 1.55, 'avg_val': 41.980769, 'max_val': 88.75, 'sum_val': 545.75, 'row_count': 13},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 0.19, 'avg_val': 26.26, 'max_val': 71.72, 'sum_val': 393.9, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 17:27:46.426156', 'min_val': 6.49, 'avg_val': 32.652667, 'max_val': 92.11, 'sum_val': 489.79, 'row_count': 15},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 18:10:46.069667', 'max_ts': '2022-03-15 23:44:46.846372', 'min_val': 2.39, 'avg_val': 33.17, 'max_val': 84.3, 'sum_val': 331.7, 'row_count': 10},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 0.59, 'avg_val': 34.506154, 'max_val': 99.51, 'sum_val': 448.58, 'row_count': 13},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 8.54, 'avg_val': 33.7975, 'max_val': 79.41, 'sum_val': 405.57, 'row_count': 12},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 17:34:47.523465', 'min_val': 8.87, 'avg_val': 45.515714, 'max_val': 95.03, 'sum_val': 637.22, 'row_count': 14},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 18:29:51.961220', 'max_ts': '2022-03-15 23:04:51.960188', 'min_val': 3.22, 'avg_val': 49.246364, 'max_val': 99.06, 'sum_val': 541.71, 'row_count': 11},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 3.79, 'avg_val': 50.540909, 'max_val': 97.07, 'sum_val': 555.95, 'row_count': 11},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 8.41, 'avg_val': 36.36, 'max_val': 81.46, 'sum_val': 363.6, 'row_count': 10},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 17:10:51.290693', 'min_val': 12.18, 'avg_val': 54.04, 'max_val': 97.21, 'sum_val': 486.36, 'row_count': 9},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 18:23:51.991431', 'max_ts': '2022-03-15 23:50:51.599394', 'min_val': 4.66, 'avg_val': 22.883333, 'max_val': 42.67, 'sum_val': 343.25, 'row_count': 15},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 0.0, 'avg_val': 34.545, 'max_val': 91.26, 'sum_val': 414.54, 'row_count': 12},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.5, 'avg_val': 16.666316, 'max_val': 72.75, 'sum_val': 316.66, 'row_count': 19},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 17:37:47.506794', 'min_val': 0.1, 'avg_val': 27.659444, 'max_val': 74.43, 'sum_val': 497.87, 'row_count': 18},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 18:18:51.620244', 'max_ts': '2022-03-15 23:09:52.732997', 'min_val': 0.22, 'avg_val': 36.611176, 'max_val': 97.33, 'sum_val': 622.39, 'row_count': 17}]

        assert asc_result != desc_result

    def test_increments_1hour(self):
        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY min_ts, device_name DESC"')

        desc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                               query=query)

        assert desc_result == [{'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 00:47:52.708401', 'min_val': 11.09, 'avg_val': 37.98, 'max_val': 64.87, 'sum_val': 75.96, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 00:16:51.264448', 'min_val': 15.64, 'avg_val': 38.525, 'max_val': 61.41, 'sum_val': 77.05, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 00:24:52.741697', 'min_val': 88.73, 'avg_val': 89.39, 'max_val': 90.05, 'sum_val': 178.78, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 00:30:47.203906', 'min_val': 42.32, 'avg_val': 42.32, 'max_val': 42.32, 'sum_val': 42.32, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 00:48:46.094775', 'min_val': 31.1, 'avg_val': 42.153333, 'max_val': 57.47, 'sum_val': 126.46, 'row_count': 3},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:01:52.374418', 'max_ts': '2022-03-15 01:20:47.517355', 'min_val': 1.96, 'avg_val': 38.13, 'max_val': 74.3, 'sum_val': 76.26, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 01:03:52.002521', 'max_ts': '2022-03-15 01:25:51.611726', 'min_val': 38.21, 'avg_val': 68.86, 'max_val': 99.51, 'sum_val': 137.72, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:17:51.617884', 'max_ts': '2022-03-15 01:48:46.391864', 'min_val': 10.59, 'avg_val': 48.61, 'max_val': 86.63, 'sum_val': 97.22, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:35:46.077756', 'max_ts': '2022-03-15 01:51:51.251381', 'min_val': 35.49, 'avg_val': 55.685, 'max_val': 75.88, 'sum_val': 111.37, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 01:59:52.742330', 'max_ts': '2022-03-15 01:59:52.742330', 'min_val': 73.41, 'avg_val': 73.41, 'max_val': 73.41, 'sum_val': 73.41, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 02:09:52.726882', 'max_ts': '2022-03-15 02:26:52.005439', 'min_val': 19.14, 'avg_val': 52.63, 'max_val': 73.43, 'sum_val': 157.89, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:10:46.426915', 'max_ts': '2022-03-15 02:30:52.394622', 'min_val': 0.59, 'avg_val': 30.836667, 'max_val': 57.07, 'sum_val': 92.51, 'row_count': 3},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:13:51.985790', 'max_ts': '2022-03-15 02:28:47.202760', 'min_val': 5.26, 'avg_val': 48.26, 'max_val': 91.26, 'sum_val': 96.52, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:18:51.970511', 'max_ts': '2022-03-15 02:49:47.525052', 'min_val': 0.78, 'avg_val': 15.6725, 'max_val': 59.42, 'sum_val': 62.69, 'row_count': 4},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 03:00:47.514114', 'max_ts': '2022-03-15 03:00:47.514114', 'min_val': 43.83, 'avg_val': 43.83, 'max_val': 43.83, 'sum_val': 43.83, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:08:51.600535', 'max_ts': '2022-03-15 03:45:47.201256', 'min_val': 0.0, 'avg_val': 6.583333, 'max_val': 10.45, 'sum_val': 19.75, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 03:24:51.285076', 'max_ts': '2022-03-15 03:24:51.285076', 'min_val': 55.57, 'avg_val': 55.57, 'max_val': 55.57, 'sum_val': 55.57, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 03:36:51.960578', 'max_ts': '2022-03-15 03:43:51.575814', 'min_val': 21.35, 'avg_val': 45.605, 'max_val': 69.86, 'sum_val': 91.21, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:02:46.852845', 'max_ts': '2022-03-15 04:19:46.423049', 'min_val': 3.79, 'avg_val': 26.62, 'max_val': 43.82, 'sum_val': 79.86, 'row_count': 3},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:17:46.083077', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 2.15, 'avg_val': 11.52, 'max_val': 32.76, 'sum_val': 46.08, 'row_count': 4},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:50:52.716817', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 44.02, 'max_val': 87.52, 'sum_val': 88.04, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 04:55:52.709587', 'max_ts': '2022-03-15 04:55:52.709587', 'min_val': 1.55, 'avg_val': 1.55, 'max_val': 1.55, 'sum_val': 1.55, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:07:51.281096', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 4.82, 'avg_val': 12.795, 'max_val': 25.66, 'sum_val': 51.18, 'row_count': 4},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:11:51.293253', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 39.6, 'max_val': 88.75, 'sum_val': 118.8, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:34:52.706622', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 44.83, 'avg_val': 66.7075, 'max_val': 97.07, 'sum_val': 266.83, 'row_count': 4},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 05:43:52.758682', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 63.59, 'avg_val': 78.49, 'max_val': 93.39, 'sum_val': 156.98, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 06:47:51.985033', 'min_val': 1.82, 'avg_val': 30.51, 'max_val': 71.54, 'sum_val': 122.04, 'row_count': 4},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 06:32:47.541993', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 06:32:51.960105', 'min_val': 21.76, 'avg_val': 21.76, 'max_val': 21.76, 'sum_val': 21.76, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 07:59:52.366762', 'min_val': 1.55, 'avg_val': 13.13, 'max_val': 35.61, 'sum_val': 39.39, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 07:17:52.374609', 'min_val': 29.05, 'avg_val': 38.2, 'max_val': 47.35, 'sum_val': 76.4, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 07:05:51.614800', 'min_val': 3.34, 'avg_val': 3.34, 'max_val': 3.34, 'sum_val': 3.34, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 07:08:46.415135', 'max_ts': '2022-03-15 07:08:46.415135', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 07:49:51.597689', 'min_val': 15.66, 'avg_val': 27.23, 'max_val': 38.8, 'sum_val': 54.46, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 08:00:46.829341', 'max_ts': '2022-03-15 08:56:46.421889', 'min_val': 0.5, 'avg_val': 6.258333, 'max_val': 10.93, 'sum_val': 37.55, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 08:01:51.567086', 'max_ts': '2022-03-15 08:01:51.567086', 'min_val': 2.57, 'avg_val': 2.57, 'max_val': 2.57, 'sum_val': 2.57, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:17:47.516724', 'max_ts': '2022-03-15 08:33:52.409299', 'min_val': 8.41, 'avg_val': 24.26, 'max_val': 39.2, 'sum_val': 72.78, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:19:47.239243', 'max_ts': '2022-03-15 08:33:52.715460', 'min_val': 23.59, 'avg_val': 40.8, 'max_val': 58.01, 'sum_val': 81.6, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 08:20:47.522034', 'max_ts': '2022-03-15 08:20:47.522034', 'min_val': 2.15, 'avg_val': 2.15, 'max_val': 2.15, 'sum_val': 2.15, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 09:06:52.762716', 'max_ts': '2022-03-15 09:34:52.366909', 'min_val': 3.65, 'avg_val': 39.47, 'max_val': 75.29, 'sum_val': 78.94, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:18:47.531564', 'max_ts': '2022-03-15 09:31:52.385871', 'min_val': 2.56, 'avg_val': 45.37, 'max_val': 71.72, 'sum_val': 136.11, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:20:51.999518', 'max_ts': '2022-03-15 09:29:46.401743', 'min_val': 10.21, 'avg_val': 20.676667, 'max_val': 32.85, 'sum_val': 62.03, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:34:52.408369', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 37.41, 'avg_val': 42.355, 'max_val': 47.3, 'sum_val': 84.71, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 09:35:51.288727', 'max_ts': '2022-03-15 09:52:52.417781', 'min_val': 18.89, 'avg_val': 41.13, 'max_val': 63.37, 'sum_val': 82.26, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:15:46.824028', 'max_ts': '2022-03-15 10:58:47.221547', 'min_val': 0.19, 'avg_val': 25.314, 'max_val': 67.37, 'sum_val': 126.57, 'row_count': 5},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:19:47.240814', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 32.0175, 'max_val': 48.19, 'sum_val': 128.07, 'row_count': 4},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 10:33:51.964373', 'max_ts': '2022-03-15 10:57:51.585040', 'min_val': 8.7, 'avg_val': 29.145, 'max_val': 49.59, 'sum_val': 58.29, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 10:36:47.549483', 'max_ts': '2022-03-15 10:50:47.518579', 'min_val': 1.42, 'avg_val': 1.87, 'max_val': 2.32, 'sum_val': 3.74, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:00:52.009794', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.91, 'avg_val': 16.528333, 'max_val': 72.75, 'sum_val': 99.17, 'row_count': 6},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 11:02:46.104113', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 5.21, 'avg_val': 5.21, 'max_val': 5.21, 'sum_val': 5.21, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 11:12:51.580880', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 26.49, 'avg_val': 53.975, 'max_val': 81.46, 'sum_val': 107.95, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:19:46.732823', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 1.53, 'avg_val': 34.895, 'max_val': 68.26, 'sum_val': 69.79, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 11:40:51.581152', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 79.41, 'avg_val': 79.41, 'max_val': 79.41, 'sum_val': 79.41, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 12:04:46.781482', 'min_val': 0.1, 'avg_val': 0.1, 'max_val': 0.1, 'sum_val': 0.1, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 12:50:52.707432', 'min_val': 6.81, 'avg_val': 42.7, 'max_val': 92.11, 'sum_val': 170.8, 'row_count': 4},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 12:42:51.304342', 'min_val': 23.97, 'avg_val': 46.77, 'max_val': 69.57, 'sum_val': 93.54, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 12:45:47.224260', 'min_val': 26.34, 'avg_val': 26.34, 'max_val': 26.34, 'sum_val': 26.34, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 12:50:46.731418', 'min_val': 33.91, 'avg_val': 33.91, 'max_val': 33.91, 'sum_val': 33.91, 'row_count': 1}]

        query = (self.base_query + ' "SELECT increments(hour, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, '
                +'min(value) as min_val, avg(value)::float(6) as avg_val, max(value) as max_val, sum(value)::float(6) as sum_val, '
                +'COUNT(*) as row_count FROM ping_sensor WHERE timestamp >= \'2022-03-15 00:00:00\' AND timestamp <= \'2022-03-15 12:59:59\' '
                +'GROUP BY device_name ORDER BY device_name, min_ts DESC"')

        asc_result = execute_query(conn=self.conn, auth=self.auth, timeout=self.timeout, destination=self.destination,
                                   query=query)

        assert asc_result == [{'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 12:11:51.592749', 'max_ts': '2022-03-15 12:42:51.304342', 'min_val': 23.97, 'avg_val': 46.77, 'max_val': 69.57, 'sum_val': 93.54, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 11:19:46.732823', 'max_ts': '2022-03-15 11:35:51.260707', 'min_val': 1.53, 'avg_val': 34.895, 'max_val': 68.26, 'sum_val': 69.79, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 10:36:47.549483', 'max_ts': '2022-03-15 10:50:47.518579', 'min_val': 1.42, 'avg_val': 1.87, 'max_val': 2.32, 'sum_val': 3.74, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 09:06:52.762716', 'max_ts': '2022-03-15 09:34:52.366909', 'min_val': 3.65, 'avg_val': 39.47, 'max_val': 75.29, 'sum_val': 78.94, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 08:20:47.522034', 'max_ts': '2022-03-15 08:20:47.522034', 'min_val': 2.15, 'avg_val': 2.15, 'max_val': 2.15, 'sum_val': 2.15, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 07:05:51.614800', 'max_ts': '2022-03-15 07:05:51.614800', 'min_val': 3.34, 'avg_val': 3.34, 'max_val': 3.34, 'sum_val': 3.34, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 06:32:47.541993', 'max_ts': '2022-03-15 06:32:47.541993', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 05:43:52.758682', 'max_ts': '2022-03-15 05:51:51.994180', 'min_val': 63.59, 'avg_val': 78.49, 'max_val': 93.39, 'sum_val': 156.98, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 04:50:52.716817', 'max_ts': '2022-03-15 04:55:46.778730', 'min_val': 0.52, 'avg_val': 44.02, 'max_val': 87.52, 'sum_val': 88.04, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 02:18:51.970511', 'max_ts': '2022-03-15 02:49:47.525052', 'min_val': 0.78, 'avg_val': 15.6725, 'max_val': 59.42, 'sum_val': 62.69, 'row_count': 4},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 01:01:52.374418', 'max_ts': '2022-03-15 01:20:47.517355', 'min_val': 1.96, 'avg_val': 38.13, 'max_val': 74.3, 'sum_val': 76.26, 'row_count': 2},
                          {'device_name': 'ADVA FSP3000R7', 'min_ts': '2022-03-15 00:09:52.001370', 'max_ts': '2022-03-15 00:16:51.264448', 'min_val': 15.64, 'avg_val': 38.525, 'max_val': 61.41, 'sum_val': 77.05, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 12:07:51.281155', 'max_ts': '2022-03-15 12:50:52.707432', 'min_val': 6.81, 'avg_val': 42.7, 'max_val': 92.11, 'sum_val': 170.8, 'row_count': 4},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 11:02:46.104113', 'max_ts': '2022-03-15 11:02:46.104113', 'min_val': 5.21, 'avg_val': 5.21, 'max_val': 5.21, 'sum_val': 5.21, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 10:15:46.824028', 'max_ts': '2022-03-15 10:58:47.221547', 'min_val': 0.19, 'avg_val': 25.314, 'max_val': 67.37, 'sum_val': 126.57, 'row_count': 5},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 09:18:47.531564', 'max_ts': '2022-03-15 09:31:52.385871', 'min_val': 2.56, 'avg_val': 45.37, 'max_val': 71.72, 'sum_val': 136.11, 'row_count': 3},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 08:01:51.567086', 'max_ts': '2022-03-15 08:01:51.567086', 'min_val': 2.57, 'avg_val': 2.57, 'max_val': 2.57, 'sum_val': 2.57, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 07:08:46.415135', 'max_ts': '2022-03-15 07:08:46.415135', 'min_val': 1.4, 'avg_val': 1.4, 'max_val': 1.4, 'sum_val': 1.4, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 06:16:46.386567', 'max_ts': '2022-03-15 06:47:51.985033', 'min_val': 1.82, 'avg_val': 30.51, 'max_val': 71.54, 'sum_val': 122.04, 'row_count': 4},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 05:11:51.293253', 'max_ts': '2022-03-15 05:50:46.090509', 'min_val': 2.05, 'avg_val': 39.6, 'max_val': 88.75, 'sum_val': 118.8, 'row_count': 3},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 04:55:52.709587', 'max_ts': '2022-03-15 04:55:52.709587', 'min_val': 1.55, 'avg_val': 1.55, 'max_val': 1.55, 'sum_val': 1.55, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 03:00:47.514114', 'max_ts': '2022-03-15 03:00:47.514114', 'min_val': 43.83, 'avg_val': 43.83, 'max_val': 43.83, 'sum_val': 43.83, 'row_count': 1},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 02:09:52.726882', 'max_ts': '2022-03-15 02:26:52.005439', 'min_val': 19.14, 'avg_val': 52.63, 'max_val': 73.43, 'sum_val': 157.89, 'row_count': 3},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 01:17:51.617884', 'max_ts': '2022-03-15 01:48:46.391864', 'min_val': 10.59, 'avg_val': 48.61, 'max_val': 86.63, 'sum_val': 97.22, 'row_count': 2},
                          {'device_name': 'Catalyst 3500XL', 'min_ts': '2022-03-15 00:31:51.300486', 'max_ts': '2022-03-15 00:48:46.094775', 'min_val': 31.1, 'avg_val': 42.153333, 'max_val': 57.47, 'sum_val': 126.46, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 12:50:46.731418', 'max_ts': '2022-03-15 12:50:46.731418', 'min_val': 33.91, 'avg_val': 33.91, 'max_val': 33.91, 'sum_val': 33.91, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 11:40:51.581152', 'max_ts': '2022-03-15 11:40:51.581152', 'min_val': 79.41, 'avg_val': 79.41, 'max_val': 79.41, 'sum_val': 79.41, 'row_count': 1},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 10:19:47.240814', 'max_ts': '2022-03-15 10:55:46.371425', 'min_val': 8.54, 'avg_val': 32.0175, 'max_val': 48.19, 'sum_val': 128.07, 'row_count': 4},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 09:20:51.999518', 'max_ts': '2022-03-15 09:29:46.401743', 'min_val': 10.21, 'avg_val': 20.676667, 'max_val': 32.85, 'sum_val': 62.03, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 08:19:47.239243', 'max_ts': '2022-03-15 08:33:52.715460', 'min_val': 23.59, 'avg_val': 40.8, 'max_val': 58.01, 'sum_val': 81.6, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 07:24:46.073295', 'max_ts': '2022-03-15 07:49:51.597689', 'min_val': 15.66, 'avg_val': 27.23, 'max_val': 38.8, 'sum_val': 54.46, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 05:07:51.281096', 'max_ts': '2022-03-15 05:24:51.249349', 'min_val': 4.82, 'avg_val': 12.795, 'max_val': 25.66, 'sum_val': 51.18, 'row_count': 4},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 03:36:51.960578', 'max_ts': '2022-03-15 03:43:51.575814', 'min_val': 21.35, 'avg_val': 45.605, 'max_val': 69.86, 'sum_val': 91.21, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 02:10:46.426915', 'max_ts': '2022-03-15 02:30:52.394622', 'min_val': 0.59, 'avg_val': 30.836667, 'max_val': 57.07, 'sum_val': 92.51, 'row_count': 3},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 01:03:52.002521', 'max_ts': '2022-03-15 01:25:51.611726', 'min_val': 38.21, 'avg_val': 68.86, 'max_val': 99.51, 'sum_val': 137.72, 'row_count': 2},
                          {'device_name': 'GOOGLE_PING', 'min_ts': '2022-03-15 00:07:46.412776', 'max_ts': '2022-03-15 00:47:52.708401', 'min_val': 11.09, 'avg_val': 37.98, 'max_val': 64.87, 'sum_val': 75.96, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 12:45:47.224260', 'max_ts': '2022-03-15 12:45:47.224260', 'min_val': 26.34, 'avg_val': 26.34, 'max_val': 26.34, 'sum_val': 26.34, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 11:12:51.580880', 'max_ts': '2022-03-15 11:17:52.720236', 'min_val': 26.49, 'avg_val': 53.975, 'max_val': 81.46, 'sum_val': 107.95, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 09:34:52.408369', 'max_ts': '2022-03-15 09:47:47.222903', 'min_val': 37.41, 'avg_val': 42.355, 'max_val': 47.3, 'sum_val': 84.71, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 08:17:47.516724', 'max_ts': '2022-03-15 08:33:52.409299', 'min_val': 8.41, 'avg_val': 24.26, 'max_val': 39.2, 'sum_val': 72.78, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 07:05:46.374750', 'max_ts': '2022-03-15 07:17:52.374609', 'min_val': 29.05, 'avg_val': 38.2, 'max_val': 47.35, 'sum_val': 76.4, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 06:32:51.960105', 'max_ts': '2022-03-15 06:32:51.960105', 'min_val': 21.76, 'avg_val': 21.76, 'max_val': 21.76, 'sum_val': 21.76, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 05:34:52.706622', 'max_ts': '2022-03-15 05:48:52.727764', 'min_val': 44.83, 'avg_val': 66.7075, 'max_val': 97.07, 'sum_val': 266.83, 'row_count': 4},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 04:02:46.852845', 'max_ts': '2022-03-15 04:19:46.423049', 'min_val': 3.79, 'avg_val': 26.62, 'max_val': 43.82, 'sum_val': 79.86, 'row_count': 3},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 03:24:51.285076', 'max_ts': '2022-03-15 03:24:51.285076', 'min_val': 55.57, 'avg_val': 55.57, 'max_val': 55.57, 'sum_val': 55.57, 'row_count': 1},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 01:35:46.077756', 'max_ts': '2022-03-15 01:51:51.251381', 'min_val': 35.49, 'avg_val': 55.685, 'max_val': 75.88, 'sum_val': 111.37, 'row_count': 2},
                          {'device_name': 'Ubiquiti OLT', 'min_ts': '2022-03-15 00:30:47.203906', 'max_ts': '2022-03-15 00:30:47.203906', 'min_val': 42.32, 'avg_val': 42.32, 'max_val': 42.32, 'sum_val': 42.32, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 12:04:46.781482', 'max_ts': '2022-03-15 12:04:46.781482', 'min_val': 0.1, 'avg_val': 0.1, 'max_val': 0.1, 'sum_val': 0.1, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 11:00:52.009794', 'max_ts': '2022-03-15 11:49:47.523295', 'min_val': 0.91, 'avg_val': 16.528333, 'max_val': 72.75, 'sum_val': 99.17, 'row_count': 6},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 10:33:51.964373', 'max_ts': '2022-03-15 10:57:51.585040', 'min_val': 8.7, 'avg_val': 29.145, 'max_val': 49.59, 'sum_val': 58.29, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 09:35:51.288727', 'max_ts': '2022-03-15 09:52:52.417781', 'min_val': 18.89, 'avg_val': 41.13, 'max_val': 63.37, 'sum_val': 82.26, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 08:00:46.829341', 'max_ts': '2022-03-15 08:56:46.421889', 'min_val': 0.5, 'avg_val': 6.258333, 'max_val': 10.93, 'sum_val': 37.55, 'row_count': 6},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 07:02:46.048736', 'max_ts': '2022-03-15 07:59:52.366762', 'min_val': 1.55, 'avg_val': 13.13, 'max_val': 35.61, 'sum_val': 39.39, 'row_count': 3},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 04:17:46.083077', 'max_ts': '2022-03-15 04:50:47.516610', 'min_val': 2.15, 'avg_val': 11.52, 'max_val': 32.76, 'sum_val': 46.08, 'row_count': 4},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 03:08:51.600535', 'max_ts': '2022-03-15 03:45:47.201256', 'min_val': 0.0, 'avg_val': 6.583333, 'max_val': 10.45, 'sum_val': 19.75, 'row_count': 3},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 02:13:51.985790', 'max_ts': '2022-03-15 02:28:47.202760', 'min_val': 5.26, 'avg_val': 48.26, 'max_val': 91.26, 'sum_val': 96.52, 'row_count': 2},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 01:59:52.742330', 'max_ts': '2022-03-15 01:59:52.742330', 'min_val': 73.41, 'avg_val': 73.41, 'max_val': 73.41, 'sum_val': 73.41, 'row_count': 1},
                          {'device_name': 'VM Lit SL NMS', 'min_ts': '2022-03-15 00:14:52.408723', 'max_ts': '2022-03-15 00:24:52.741697', 'min_val': 88.73, 'avg_val': 89.39, 'max_val': 90.05, 'sum_val': 178.78, 'row_count': 2}]

        assert desc_result != asc_result

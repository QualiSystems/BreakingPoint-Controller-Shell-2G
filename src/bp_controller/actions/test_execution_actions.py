from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class TestExecutionActions(object):
    def __init__(self, rest_service, logger):
        """
        Reboot actions
        :param rest_service:
        :type rest_service: RestJsonClient
        :param logger:
        :type logger: Logger
        :return:
        """
        self._rest_service = rest_service
        self._logger = logger

    def start_test(self, test_name):
        self._logger.debug('Starting test {}'.format(test_name))
        uri = 'api/v1/bps/tests/operations/start'
        json_data = {"modelname": test_name, "group": "1"}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result

    def stop_test(self, test_id):
        self._logger.debug('Stop running, testID {}'.format(test_id))
        uri = '/api/v1/bps/tests/operations/stop'
        json_data = {"testid": test_id}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result

    def get_real_time_statistics(self, test_id, stats_group='summary'):
        self._logger.debug('Get RTS, testID {0}, {1}'.format(test_id, stats_group))
        uri = '/api/v1/bps/tests/operations/getrts'
        json_request = {'runid': test_id, 'statsGroup': stats_group}
        data = self._rest_service.request_post(uri, json_request)
        result = data
        return result

    def get_results(self, test_id):
        self._logger.debug('Stop running, testID {}'.format(test_id))
        uri = '/api/v1/bps/tests/operations/result'
        json_request = {'runid': test_id}
        data = self._rest_service.request_post(uri, json_request)
        result = data
        return result

    def running_tests(self):
        self._logger.debug('Running tests')
        uri = '/api/v1/bps/tests'
        data = self._rest_service.request_get(uri)
        result = data
        return result

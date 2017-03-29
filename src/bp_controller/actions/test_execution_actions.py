from cloudshell.tg.breaking_point.rest_actions.exceptions import RestActionsException
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

    def start_test(self, test_name, group_id):
        self._logger.debug('Starting test {}'.format(test_name))
        uri = 'api/v1/bps/tests/operations/start'
        json_data = {"modelname": test_name, "group": group_id}
        data = self._rest_service.request_post(uri, json_data)
        test_id = data.get('testid')
        return test_id

    def stop_test(self, test_id):
        self._logger.debug('Stop running, testID {}'.format(test_id))
        uri = '/api/v1/bps/tests/operations/stop'
        json_data = {"testid": test_id}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        return result

    def get_test_status(self, test_id):
        self._logger.debug('Geting test status, testID {}'.format(test_id))
        uri = '/api/v1/bps/tests/operations/result'
        json_request = {'runid': test_id}
        data = self._rest_service.request_post(uri, json_request)
        result = data.get('result')
        return result

    def running_tests(self):
        self._logger.debug('Running tests')
        uri = '/api/v1/bps/tests'
        data = self._rest_service.request_get(uri)
        result = data
        return result

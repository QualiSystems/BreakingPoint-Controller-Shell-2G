from cloudshell.tg.breaking_point.rest_actions.exceptions import RestActionsException
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class TestStatisticsActions(object):
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

    def get_real_time_statistics(self, test_id, stats_group='summary'):
        self._logger.debug('Get RTS, testID {0}, {1}'.format(test_id, stats_group))
        uri = '/api/v1/bps/tests/operations/getrts'
        json_request = {'runid': test_id, 'statsGroup': stats_group}
        data = self._rest_service.request_post(uri, json_request)
        result = data
        return result

    def get_result_file(self, test_id, result_format):
        self._logger.debug('Running tests')
        if result_format not in ['pdf', 'csv', 'rtf', 'html', 'xml', 'zip']:
            raise RestActionsException(self.__class__.__name__, 'Incorrect format {}'.format(result_format))
        uri = '/api/v1/bps/export/report/{0}/{1}'.format(test_id, result_format)
        data = self._rest_service.request_get(uri)
        result = data
        return result

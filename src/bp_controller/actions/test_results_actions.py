import zipfile
import io

from cloudshell.tg.breaking_point.rest_actions.exceptions import RestActionsException
from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class TestResultsActions(object):
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

    def get_result_file(self, test_id, result_format):
        self._logger.debug('Get result in format {}'.format(result_format))
        if result_format not in ['pdf', 'csv', 'rtf', 'html', 'xml', 'zip']:
            raise RestActionsException(self.__class__.__name__, 'Incorrect format {}'.format(result_format))
        uri = '/api/v1/bps/export/report/{0}/{1}'.format(test_id, result_format)
        data = self._rest_service.request_get_files(uri)
        return data.content

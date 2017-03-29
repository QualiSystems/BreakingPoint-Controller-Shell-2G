from threading import Lock

_NETWORK_ACTIONS_LOCK = Lock()


class TestNetworkActions(object):
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

    def get_network_neighborhood(self, name):
        self._logger.debug('Network info {0}'.format(name))
        with _NETWORK_ACTIONS_LOCK:
            uri_r = '/api/v1/bps/network/operations/retrieve'
            request_body = {'name': name}
            self._rest_service.request_post(uri_r, request_body)
            uri_g = '/api/v1/bps/network/'
            data = self._rest_service.request_get(uri_g)
            result = data.get('interfaces')
            return result

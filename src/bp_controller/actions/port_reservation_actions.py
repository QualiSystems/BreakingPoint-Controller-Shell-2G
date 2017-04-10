from cloudshell.tg.breaking_point.rest_api.rest_json_client import RestJsonClient


class PortReservationActions(object):
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

    def port_status(self):
        uri = '/api/v1/bps/ports'
        data = self._rest_service.request_get(uri)
        result = data.get('portReservationState')
        self._logger.debug('Port status {}'.format(result))
        return result

    def reserve_port(self, slot, port_list, group):
        self._logger.debug('Reserving ports {0} on slot {1} for group {2}'.format(port_list, slot, group))
        uri = '/api/v1/bps/ports/operations/reserve'
        json_data = {"slot": slot, "portList": port_list, "group": group, "force": "true"}
        self._logger.info(json_data)
        data = self._rest_service.request_post(uri, json_data)
        result = data
        self._logger.debug(str(result))
        return result

    def unreserve_port(self, slot, port_list):
        self._logger.debug('Unreserving ports {0} on slot {1}'.format(port_list, slot))
        uri = '/api/v1/bps/ports/operations/unreserve'
        json_data = {"slot": slot, "portList": port_list}
        data = self._rest_service.request_post(uri, json_data)
        result = data
        self._logger.debug(str(result))
        return result

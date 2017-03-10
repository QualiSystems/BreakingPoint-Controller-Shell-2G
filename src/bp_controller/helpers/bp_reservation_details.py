import re


class BPReservationDetails(object):
    PORT_FAMILY = 'Port'
    PORT_ATTRIBUTE = 'Logical Name'

    def __init__(self, context, logger, api):
        self._context = context
        self._logger = logger
        self._api = api

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        self._context = value

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        self._api = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @property
    def _reservation_details(self):
        reservation_id = self.context.reservation.reservation_id
        return self.api.GetReservationDetails(reservationId=reservation_id)

    def get_chassis_ports(self):
        reserved_ports = {}
        port_pattern = r'{}/M(?P<module>\d+)/P(?P<port>\d+)'.format(self.context.resource.address)
        for resource in self._reservation_details.ReservationDescription.Resources:
            if resource.ResourceFamilyName == self.PORT_FAMILY:
                result = re.match(port_pattern, resource.FullAddress)
                if result:
                    logical_name = self.api.GetAttributeValue(resourceFullPath=resource.Name,
                                                              attributeName=self.PORT_ATTRIBUTE).Value
                    if logical_name:
                        reserved_ports[logical_name.lower()] = (result.group('module'), result.group('port'))
        return reserved_ports

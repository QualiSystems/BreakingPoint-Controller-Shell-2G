class BPReservationDetails(object):
    CHASSIS_FAMILY = 'Traffic Generator Chassis'
    # MODULE_FAMILY = 'Module'
    PORT_FAMILY = 'Port'

    def __init__(self, context, logger, api):
        self._context = context
        self._logger = logger
        self._api = api

    @property
    def _reservation_details(self):
        reservation_id = self._context.reservation.reservation_id
        return self._api.GetReservationDetails(reservationId=reservation_id)

    def get_chassis_ports(self):
        chassis_objs_dict = dict()
        ports_obj = []
        # resource_details = self._api.GetResourceDetails('10.5.1.127')
        for resource in self._reservation_details.ReservationDescription.Resources:
            if resource.ResourceFamilyName == self.CHASSIS_FAMILY:
                chassis_objs_dict[resource.FullAddress] = {'chassis': resource, 'ports': list()}
                #
                #     elif resource.ResourceFamilyName == self.PORT_FAMILY:
                #         chassis_adr = resource.FullAddress.split('/')[0]
                #         if chassis_adr in chassis_objs_dict:
                #             chassis_objs_dict[chassis_adr]['ports'].append(resource)
                #             ports_obj.append(resource)
                #
                # ports_obj_dict = dict()
                # for port in ports_obj:
                #     val = my_api.GetAttributeValue(resourceFullPath=port.Name, attributeName="Logical Name").Value
                #     if val:
                #         port.logic_name = val
                #         ports_obj_dict[val.lower().strip()] = port
                # if not ports_obj_dict:
                #     self.logger.error("You should add logical name for ports")
                #     raise Exception("You should add logical name for ports")

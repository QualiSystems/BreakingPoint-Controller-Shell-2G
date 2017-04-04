from collections import defaultdict
from bp_controller.flows.bp_port_reservation_flow import BPPortReservationFlow
from cloudshell.tg.breaking_point.bp_exception import BPException
from cloudshell.tg.breaking_point.runners.exceptions import BPRunnerException


class PortReservationHelper(object):
    GROUP_MIN = 1
    GROUP_MAX = 12

    def __init__(self, session_manager, cs_reservation_details, logger):
        """
        :param session_manager:
        :type
        :param cs_reservation_details:
        :param logger:
        :return:
        """
        self._session_manager = session_manager
        self._logger = logger
        self._cs_reservation_details = cs_reservation_details

        self.__reservation_flow = None
        self.__group_id = None
        self.__reserved_ports = None

    @property
    def group_id(self):
        return self.__group_id

    @property
    def _reservation_flow(self):
        """
        :return:
        :rtype: BPPortReservationFlow
        """
        if not self.__reservation_flow:
            self.__reservation_flow = BPPortReservationFlow(self._session_manager, self._logger)
        return self.__reservation_flow

    def _get_groups_info(self):
        groups_info = defaultdict(list)
        for port_info in self._reservation_flow.port_status():
            group_id = port_info.get('group')
            if group_id is not None:
                groups_info[int(group_id)].append((port_info['slot'], port_info['port']))
        return groups_info

    def _find_not_used_group_id(self):
        available_groups = list(
            set([i for i in xrange(self.GROUP_MIN, self.GROUP_MAX + 1)]) - set(self._get_groups_info().keys()))
        if len(available_groups) > 0:
            group_id = sorted(available_groups)[0]
        else:
            raise Exception(self.__class__.__name__, 'Not available groups to reserve')
        return group_id

    def _find_used_group_id(self, port_order):
        appropriate_group = None
        groups_info = self._get_groups_info()
        port_order_set = set(port_order)
        for group, ports in groups_info.iteritems():
            ports_set = set(ports)
            if port_order_set == ports_set:
                appropriate_group = group
                break
        return appropriate_group

    def reserve_ports(self, network_name, interfaces):
        # associating ports
        bp_test_interfaces = self._reservation_flow.get_interfaces(network_name) if network_name else {}
        cs_reserved_ports = self._cs_reservation_details.get_chassis_ports()

        reservation_order = []
        self._logger.debug('CS reserved ports {}'.format(cs_reserved_ports))
        self._logger.debug('BP test interfaces {}'.format(bp_test_interfaces))
        for int_number in sorted(interfaces):
            bp_interface = bp_test_interfaces.get(int_number, None)
            if bp_interface and bp_interface in cs_reserved_ports:
                self._logger.debug('Associating interface {}'.format(bp_interface))
                reservation_order.append(cs_reserved_ports[bp_interface])
            else:
                raise BPRunnerException(self.__class__.__name__,
                                        'Cannot find Port with Logical name {} in the reservation'.format(bp_interface))

        # Find correct group and reserve
        if self.__group_id is not None:
            not_used_ports = set(self.__reserved_ports) - set(reservation_order)
            self._reservation_flow.unreserve_ports(not_used_ports)

            to_be_reserved = set(reservation_order) - set(self.__reserved_ports)
            self._reservation_flow.reserve_ports(self.__group_id, to_be_reserved)

            self.__reserved_ports = reservation_order
        else:
            used_group_id = self._find_used_group_id(reservation_order)
            if used_group_id is None:
                self.__group_id = self._find_not_used_group_id()
                self._reservation_flow.reserve_ports(self.__group_id, reservation_order)
            else:
                self.__group_id = used_group_id
        self.__reserved_ports = reservation_order
        return self.__group_id

    def unreserve_ports(self):
        self.__group_id = None
        if self.__reserved_ports:
            self._reservation_flow.unreserve_ports(self.__reserved_ports)
            self.__reserved_ports = None

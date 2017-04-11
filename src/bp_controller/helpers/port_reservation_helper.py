from collections import defaultdict
from bp_controller.flows.bp_port_reservation_flow import BPPortReservationFlow
from bp_controller.helpers.bp_cs_reservation_details import BPCSReservationDetails
from bp_controller.utils.file_based_lock import FileBasedLock
from cloudshell.tg.breaking_point.bp_exception import BPException


class PortReservationHelper(object):
    GROUP_MIN = 1
    GROUP_MAX = 12
    LOCK_FILE = '.port_reservation.lock'

    def __init__(self, session_context_manager, cs_reservation_details, logger):
        """
        :param session_manager:
        :type
        :param cs_reservation_details:
        :type cs_reservation_details: BPCSReservationDetails
        :param logger:
        :return:
        """
        self._session_context_manager = session_context_manager
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
            self.__reservation_flow = BPPortReservationFlow(self._session_context_manager, self._logger)
        return self.__reservation_flow

    def _get_groups_info(self):
        """
        Collect information regarding used groups
        :return:
        """
        groups_info = defaultdict(list)
        for port_info in self._reservation_flow.port_status():
            group_id = port_info.get('group')
            if group_id is not None:
                groups_info[int(group_id)].append((port_info['slot'], port_info['port']))
        return groups_info

    def _find_not_used_group_id(self):
        """
        Find not used group id
        :return:
        """
        available_groups = list(
            set([i for i in xrange(self.GROUP_MIN, self.GROUP_MAX + 1)]) - set(self._get_groups_info().keys()))
        if len(available_groups) > 0:
            group_id = sorted(available_groups)[0]
        else:
            raise BPException(self.__class__.__name__, 'Cannot find unused group id')
        return group_id

    def _find_used_ports(self, port_order):
        """
        Find port usage
        :param port_order:
        :return:
        """
        used_ports = []
        groups_info = self._get_groups_info()
        port_order_set = set(port_order)
        for ports in groups_info.values():
            used_ports_set = set(ports) & port_order_set
            used_ports.extend(list(used_ports_set))
        return used_ports

    def _build_reservation_order(self, network_name, interfaces):
        """
        Associate BP interfaces with CS ports and build reservation order
        :param network_name:
        :param interfaces:
        :return:
        """
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
                raise BPException(self.__class__.__name__,
                                  'Cannot find Port with Logical name {} in the reservation'.format(bp_interface))
        return reservation_order

    def reserve_ports(self, network_name, interfaces):
        """
        Reserve ports
        :param network_name:
        :param interfaces:
        :return:
        """

        reservation_order = self._build_reservation_order(network_name, interfaces)

        # Unreserve used ports and reserve new port order
        with FileBasedLock(self.LOCK_FILE):
            self.unreserve_ports()
            used_ports = self._find_used_ports(reservation_order)
            self._reservation_flow.unreserve_ports(used_ports)
            self.__group_id = self._find_not_used_group_id()
            self._reservation_flow.reserve_ports(self.__group_id, reservation_order)
            self.__reserved_ports = reservation_order

    def unreserve_ports(self):
        """
        Unreserve ports
        :return:
        """
        self.__group_id = None
        if self.__reserved_ports:
            self._reservation_flow.unreserve_ports(self.__reserved_ports)
            self.__reserved_ports = None

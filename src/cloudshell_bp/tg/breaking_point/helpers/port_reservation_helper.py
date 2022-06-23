from collections import defaultdict

from cloudshell_bp.tg.breaking_point.bp_exception import BPException
from cloudshell_bp.tg.breaking_point.helpers.bp_cs_reservation_details import BPCSReservationDetails
from cloudshell_bp.tg.breaking_point.utils.file_based_lock import FileBasedLock


class PortReservationHelper(object):
    GROUP_MIN = 1
    GROUP_MAX = 12
    LOCK_FILE = ".port_reservation.lock"

    def __init__(self, reservation_flow, cs_reservation_details, logger):
        """
        :type reservation_flow: cloudshell.tg.breaking_point.flows.bp_port_reservation_flow.BPPortReservationFlow
        :type cs_reservation_details: BPCSReservationDetails
        :type logger: logging.Logger
        """
        self._reservation_flow = reservation_flow
        self._logger = logger
        self._cs_reservation_details = cs_reservation_details

    def _get_groups_info(self):
        """
        Collect information regarding used groups
        :return:
        """
        groups_info = defaultdict(list)
        for port_info in self._reservation_flow.port_status():
            group_id = port_info.get("group")
            if group_id is not None:
                groups_info[int(group_id)].append((port_info["slot"], port_info["port"]))
        return groups_info

    def _find_not_used_group_id(self):
        """
        Find not used group id
        :return:
        """
        available_groups = list(
            set([i for i in range(self.GROUP_MIN, self.GROUP_MAX + 1)]) - set(self._get_groups_info().keys())
        )
        if len(available_groups) > 0:
            group_id = sorted(available_groups)[0]
        else:
            raise BPException(self.__class__.__name__, "Cannot find unused group id")
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
        self._logger.debug("CS reserved ports {}".format(cs_reserved_ports))
        self._logger.debug("BP test interfaces {}".format(bp_test_interfaces))
        for int_number in sorted(interfaces):
            bp_interface = bp_test_interfaces.get(int_number, None)
            if bp_interface and bp_interface in cs_reserved_ports:
                self._logger.debug("Associating interface {}".format(bp_interface))
                reservation_order.append(cs_reserved_ports[bp_interface])
            else:
                raise BPException(
                    self.__class__.__name__, "Cannot find Port with Logical name {} in the reservation".format(bp_interface)
                )
        return reservation_order

    def reserve_ports(self, network_name, interfaces, bp_session):
        """
        Reserve ports
        :type bp_session: cloudshell.tg.breaking_point.entities.bp_session.BPSession
        :param network_name:
        :param interfaces:
        :return:
        """

        reservation_order = self._build_reservation_order(network_name, interfaces)

        # Unreserve used ports and reserve new port order
        with FileBasedLock(self.LOCK_FILE):
            self.unreserve_ports(bp_session)
            used_ports = self._find_used_ports(reservation_order)
            self._reservation_flow.unreserve_ports(used_ports)
            group_id = self._find_not_used_group_id()
            self._reservation_flow.reserve_ports(group_id, reservation_order)
            bp_session.reservation_group = group_id
            bp_session.reserved_ports = reservation_order
            return bp_session

    def unreserve_ports(self, bp_session):
        """
        Unreserve ports
        :type bp_session: cloudshell.tg.breaking_point.entities.bp_session.BPSession

        """
        bp_session.reservation_group = None
        if bp_session.reserved_ports:
            self._reservation_flow.unreserve_ports(bp_session.reserved_ports)
            bp_session.reserved_ports = None
        return bp_session

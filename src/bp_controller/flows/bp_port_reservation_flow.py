from bp_controller.actions.test_network_actions import TestNetworkActions
from cloudshell.tg.breaking_point.flows.exceptions import BPFlowException
import re
from xml.etree import ElementTree
from bp_controller.actions.port_reservation_actions import PortReservationActions
from bp_controller.actions.test_configuration_actions import TestConfigurationActions
from bp_controller.actions.test_execution_actions import TestExecutionActions
from cloudshell.tg.breaking_point.flows.bp_flow import BPFlow


class BPPortReservationFlow(BPFlow):
    def port_status(self):
        with self._session_context_manager as rest_service:
            port_reservation = PortReservationActions(rest_service, self._logger)
            ports_info = port_reservation.port_status()
            port_expression = r'\[slot=(?P<slot>\d+),port=(?P<port>\d+)\]=\d+' \
                              r'(:\[reserved=(?P<reserved>\w+),group=(?P<group>\d+),number=(?P<number>\d+)\])?'

            result = []
            for group in re.finditer(port_expression, ports_info):
                result.append(group.groupdict())
            return result

    def get_interfaces(self, network_name):
        if network_name:
            with self._session_context_manager as rest_service:
                test_network_actions = TestNetworkActions(rest_service, self._logger)
                network_info = test_network_actions.get_network_neighborhood(network_name)
            test_interfaces = {}
            for key, value in network_info.iteritems():
                interface_id = key.split(':')[1]
                result = re.search(r'number:\s*(?P<id>\d+)', value, re.IGNORECASE)
                if result:
                    number = result.group('id')
                    test_interfaces[int(number)] = str(interface_id).lower()
                else:
                    BPFlowException(self.__class__.__name__, 'Interface number is not defined')
            return test_interfaces
        else:
            raise BPFlowException(self.__class__.__name__, 'Network name cannot be empty')

    def reserve_ports(self, group, ports):
        with self._session_context_manager as rest_service:
            port_reservation = PortReservationActions(rest_service, self._logger)
            results = []
            for slot, port in ports:
                result = port_reservation.reserve_port(slot, [port], group)

    def unreserve_ports(self, ports):
        with self._session_context_manager as rest_service:
            port_reservation = PortReservationActions(rest_service, self._logger)
            results = []
            for slot, port in ports:
                result = port_reservation.unreserve_port(slot, [port])
